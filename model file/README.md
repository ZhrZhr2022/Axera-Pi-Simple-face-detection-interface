
# Detection model generated by MaixHub for AXera Pi

| 中文在下方 |

## Labels

"LZY", "ZHR"

## Inputs

layer name: shape(hwc)

* input0: (224, 224, 3)

## Outputs

layer name: shape(hwc)

* output0: (28, 28, 21)
* output1: (14, 14, 21)
* output2: (7, 7, 21)

## Anchors

[10, 13, 16, 30, 33, 23, 30, 61, 62, 45, 59, 119, 116, 90, 156, 198, 373, 326]

## Usage

Download [maix-iii-axera-pi_maixhub_model_runner_demo](https://maixhub.com/model/zoo/93),
and unzip, there's a readme file in it, follow the readme to run the demo.
> Just copy the `model.joint` and `yolov5s.json` file and the executable file in this zip to board, and run it:
> `chmod +x sample_vin_ivps_joint_venc_rtsp_vo`
> `./sample_vin_ivps_joint_venc_rtsp_vo -p yolov5s.json -c 2`

The board basic usage(like how to copy files to board) refer to [Maix-III AXera-Pi Doc](https://wiki.sipeed.com/m3axpi).

And you can also refer to [YOLOv5s 80 types objects detection](https://maixhub.com/model/zoo/93).


## Others

More info refer to report.json file

--------------

# 从 MaixHub 生成的适用于 AXera Pi 的检测模型 (中文在下方)

## 标签

"LZY", "ZHR"

## 输入层信息

层名称: 形状(hwc)

* input0: (224, 224, 3)

## 输出层信息

层名称: 形状(hwc)

* output0: (28, 28, 21)
* output1: (14, 14, 21)
* output2: (7, 7, 21)

## Anchors

[10, 13, 16, 30, 33, 23, 30, 61, 62, 45, 59, 119, 116, 90, 156, 198, 373, 326]

## 使用方法

下载 [maix-iii-axera-pi_maixhub_model_runner_demo](https://maixhub.com/model/zoo/93),
解压, 里面有个 readme 文件, 根据里面的使用说明运行模型。
> 拷贝 `model.joint` 和 `yolov5s.json` 文件 以及压缩包中的可执行文件到开发板，并运行:
> `chmod +x sample_vin_ivps_joint_venc_rtsp_vo`
> `./sample_vin_ivps_joint_venc_rtsp_vo -p yolov5s.json -c 2`

板子的基本用法（比如如何拷贝文件到开发板）请参考 [Maix-III AXera-Pi Doc](https://wiki.sipeed.com/m3axpi)。

另外也可以参考 [YOLOv5s 80 types objects detection](https://maixhub.com/model/zoo/93)。


## 其它

更多模型信息参考 report.json 文件
