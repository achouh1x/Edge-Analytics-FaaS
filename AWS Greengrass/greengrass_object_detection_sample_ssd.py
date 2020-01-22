#!/usr/bin/env python
"""
 Copyright (C) 2018-2019 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

from __future__ import print_function
import sys
import os
from argparse import ArgumentParser, SUPPRESS
import cv2
import time
import logging as log
import numpy as np
import datetime
import threading
import greengrasssdk
import boto3
import json
from collections import OrderedDict

from openvino.inference_engine import IENetwork, IECore, IEPlugin


# Specify the delta in seconds between each report
sys_interval = 5.0

# Parameters for IoT Cloud
enable_iot_cloud_output = True

# Parameters for Kinesis
enable_kinesis_output = False
kinesis_stream_name = ""
kinesis_partition_key = ""
kinesis_region = ""

# Parameters for S3
enable_s3_jpeg_output = False
s3_bucket_name = "ssd_test"

# Parameters for jpeg output on local disk
enable_local_jpeg_output = False

# Create a Greengrass Core SDK client for publishing messages to AWS Cloud
client = greengrasssdk.client("iot-data")

# Create an S3 client for uploading files to S3
if enable_s3_jpeg_output:
    s3_client = boto3.client("s3")

# Create a Kinesis client for putting records to streams
if enable_kinesis_output:
    kinesis_client = boto3.client("kinesis", "us-east-2")


PARAM_MODEL_XML = os.environ.get("PARAM_MODEL_XML")
PARAM_INPUT_SOURCE = os.environ.get("PARAM_INPUT_SOURCE")
PARAM_DEVICE = os.environ.get("PARAM_DEVICE")
PARAM_OUTPUT_DIRECTORY = os.environ.get("PARAM_OUTPUT_DIRECTORY")
PARAM_CPU_EXTENSION_PATH = os.environ.get("PARAM_CPU_EXTENSION_PATH")
PARAM_LABELMAP_FILE = os.environ.get("PARAM_LABELMAP_FILE")
PARAM_TOPIC_NAME = os.environ.get("PARAM_TOPIC_NAME", "intel/faas/ssd")
PARAM_PROB_THRESHOLD = os.environ.get("PARAM_PROB_THRESHOLD")

# Comment out these lines to enable using custom batch size, number of streams, and number of requests.
# Batch size should be divisors of number of streams. (If number of streams is 16, batch size should be either 1, 2, 4, 8, or 16)
#PARAM_BATCH_SIZE = os.environ.get("PARAM_BATCH_SIZE")
#PARAM_NUM_REQUESTS = os.environ.get("PARAM_NUM_REQUESTS")
#PARAM_NUM_STREAMS = os.environ.get("PARAM_NUM_STREAMS")

# Use the fixed batch size, number of requests, and number of streams for a AWS Greengrass demo with a single input.
PARAM_BATCH_SIZE = 1
PARAM_NUM_REQUESTS = 16
PARAM_NUM_STREAMS = 1


def report(res_json, frames):
    now = datetime.datetime.now()
    date_prefix = str(now).replace(" ", "_")
    if enable_iot_cloud_output:
        data = json.dumps(res_json)
        client.publish(topic=PARAM_TOPIC_NAME, payload=data)
    if enable_kinesis_output:
        kinesis_client.put_record(StreamName=kinesis_stream_name, Data=json.dumps(res_json), PartitionKey=kinesis_partition_key)
    if enable_s3_jpeg_output:
        s = 0
        for frame in frames:
            temp_image = os.path.join(PARAM_OUTPUT_DIRECTORY, "inference_result.jpeg")
            cv2.imwrite(temp_image, frame)
            with open(temp_image) as file:
                image_contents = file.read()
                s3_client.put_object(Body=image_contents, Bucket=s3_bucket_name, Key="stream" + str(s) + "_" +date_prefix + ".jpeg")
            s += 1
    if enable_local_jpeg_output:
        s = 0
        for frame in frames:
            cv2.imwrite(os.path.join(PARAM_OUTPUT_DIRECTORY, "stream" + str(s) + "_" + date_prefix + ".jpeg"), frame)
            s += 1


def greengrass_object_detection_sample_ssd_run():
    client = greengrasssdk.client("iot-data")
    client.publish(topic=PARAM_TOPIC_NAME, payload="Greengrass Object Detection Sample on OpenVINO R3.1")
    model_xml = PARAM_MODEL_XML
    model_bin = os.path.splitext(PARAM_MODEL_XML)[0] + ".bin"
    n_streams = int(PARAM_NUM_STREAMS)
    b_size = int(PARAM_BATCH_SIZE)
    n_requests = int(PARAM_NUM_REQUESTS)
    prob_threshold = float(PARAM_PROB_THRESHOLD)
    input_stream = []
    cap = []
    req_frames = []
    frames_out = []
    req_ids = []
    inf_start = []
    inf_frames = []
    inf_fps = []
    inf_time = []
    num_frames = []
    req_stride = n_streams/b_size
    plugin = IEPlugin(device=PARAM_DEVICE, plugin_dirs="")

    log.info("Creating Inference Engine...")
    if "CPU" in PARAM_DEVICE:
        plugin.add_cpu_extension(PARAM_CPU_EXTENSION_PATH)
    # Read IR
    log.info("Loading network files:\n\t{}\n\t{}".format(model_xml, model_bin))
    net = IENetwork(model=model_xml, weights=model_bin)
    print("Batch Size: "+str(net.batch_size))

    img_info_input_blob = None
    feed_dict = {}
    for blob_name in net.inputs:
        if len(net.inputs[blob_name].shape) == 4:
            input_blob = blob_name
        elif len(net.inputs[blob_name].shape) == 2:
            img_info_input_blob = blob_name
        else:
            raise RuntimeError("Unsupported {}D input layer '{}'. Only 2D and 4D input layers are supported"
                               .format(len(net.inputs[blob_name].shape), blob_name))

    assert len(net.outputs) == 1, "Demo supports only single output topologies"

    out_blob = next(iter(net.outputs))
    client.publish(topic=PARAM_TOPIC_NAME, payload="Loading IR to the plugin...")
    exec_net = plugin.load(network=net, num_requests=n_requests)
    # Read and pre-process input image
    n, c, h, w = net.inputs[input_blob].shape
    if img_info_input_blob:
        feed_dict[img_info_input_blob] = [h, w, 1]

    if PARAM_INPUT_SOURCE == 'cam':
        input_stream = 0
    else:
        for s in range(n_streams):
            frames_out.append(0)
            # Comment out the line below to use multiple streams. PARAM_INPUT_SOURCE should be path/to/dir/video_series_name where video file names are video_series_name0.mp4, video_series_name1.mp4, and so on.
            #input_stream.append(PARAM_INPUT_SOURCE+str(s)+".mp4")
            # Use the line below for single input file. PARAM_INPUT_SOURCE should be the path to a video file or a video device.
            input_stream.append(PARAM_INPUT_SOURCE)
            assert os.path.isfile(input_stream[s]), "Specified input file doesn't exist"
    labels_map = None

    for s in range(n_streams):
        cap.append(cv2.VideoCapture(input_stream[s]))

    for r in range(n_requests):
        req_ids.append(r)
        req_frames.append([])
        inf_start.append(0)
        inf_time.append(0)
        inf_fps.append(0)
        num_frames.append(0)

    client.publish(topic=PARAM_TOPIC_NAME, payload="Starting inference...")
    is_async_mode = False
    render_time = 0

    sys_time = time.time()
    sys_frames = 0
    output_time = time.time()
    r = 0
    running = True
    while running:
        in_batch = np.zeros((b_size, c, h, w))
        frames = []
        for b in range(b_size):
            s = ((r%req_stride)*b_size)+b
            if cap[s].isOpened():
                ret, frame = cap[s].read()
                if not ret:
                    cap[s].set(2, 0)
                    ret, frame = cap[s].read()
                frames.append(frame)
                initial_w = cap[s].get(3)
                initial_h = cap[s].get(4)
                in_frame = cv2.resize(frames[b], (w, h))
                in_frame = in_frame.transpose((2, 0, 1))  # Change data layout from HWC to CHW
                in_frame = in_frame.reshape((1, c, h, w))
                in_batch[b] = in_frame[0]
        if len(frames) == b_size:
            req_frames[req_ids[r]] = frames
            feed_dict[input_blob] = in_batch
            inf_start[r] = time.time()
            exec_net.start_async(request_id=req_ids[r], inputs=feed_dict)
            r = (r+1)%n_requests
            if inf_start[r] != 0 and exec_net.requests[req_ids[r]].wait(-1) == 0:
                sys_frames += b_size

                # Parse detection results of the current request
                res_json = OrderedDict()
                timestamp = datetime.datetime.now()
                res = exec_net.requests[req_ids[r]].outputs[out_blob]
                object_id = 0
                for obj in res[0][0]:
                    # Draw only objects when probability more than specified threshold
                    if obj[2] > prob_threshold and obj[0] < n_streams and obj[0] >= 0:
                        b = int(obj[0])
                        xmin = int(obj[3] * initial_w)
                        ymin = int(obj[4] * initial_h)
                        xmax = int(obj[5] * initial_w)
                        ymax = int(obj[6] * initial_h)
                        class_id = int(obj[1])
                        # Draw box and label\class_id
                        color = (min(class_id * 12.5, 255), min(class_id * 7, 255), min(class_id * 5, 255))
                        if class_id == 2:
                            color = (255, 0, 0)
                        elif class_id == 3:
                            color = (0, 255, 0)
                        elif class_id == 5:
                            color = (0, 255, 255)
                        if ((xmin | ymin | xmax | ymax) & ~0xFFFF == 0) and (xmin < xmax) and (ymin < ymax) and b < b_size:
                            cv2.rectangle(req_frames[r][b], (xmin, ymin), (xmax, ymax), color, 2)
                            det_label = labels_map[class_id] if labels_map else str(class_id)
                            cv2.putText(req_frames[r][b], det_label + ' ' + str(round(obj[2] * 100, 1)) + ' %', (xmin, ymin - 7),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, color, 1)
                            obj_id = "Object" + str(object_id)
                            stream_offset = r%req_stride
                            s = (stream_offset*b_size)+b
                            res_json[obj_id] = {"stream": s, "label": int(obj[1]), "class": det_label, "confidence": round(obj[2], 2),
                                    "xmin": round(obj[3], 2), "ymin": round(obj[4], 2), "xmax": round(obj[5], 2), "ymax": round(obj[6], 2)}
                            object_id += 1

                stream_offset = r%req_stride
                for b in range(b_size):
                    frames_out[(stream_offset*b_size)+b] = req_frames[r][b]

            sys_elapsed = time.time()-sys_time
            if (sys_elapsed >= sys_interval):
                sys_fps = sys_frames / sys_elapsed
                sys_time = time.time()
                sys_frames = 0
                res_json["timestamp"] = timestamp.isoformat()
                res_json["system_fps"] = sys_fps
                reportThread = threading.Thread(target=report, args=(res_json, frames_out,))
                reportThread.start()
                #client.publish(topic=PARAM_TOPIC_NAME, payload="Reported System FPS: "+str(sys_fps))


greengrass_object_detection_sample_ssd_run()


def function_handler(event, context):
    client.publish(topic=PARAM_TOPIC_NAME, payload='HANDLER_CALLED!')
    return
