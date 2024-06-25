#include "asr.h"
extern "C"{ void * __dso_handle = 0 ;}
#include "setup.h"
#include "HardwareSerial.h"
#include "myLib/asr_event.h"

uint32_t snid;
String Rec = "";
void ASR_CODE();

//{speak:小蝶-清新女声,vol:4,speed:10,platform:haohaodada}
//{playid:10001,voice:}
//{playid:10002,voice:}

/*描述该功能...
*/
void ASR_CODE(){
  //本函数是语音识别成功钩子程序
  //运行时间越短越好，复杂控制启动新线程运行
  //唤醒时间设置必须在ASR_CODE中才有效
  //用switch分支选择，根据不同的识别成功的ID执行相应动作，点击switch左上齿轮
  //可以增加分支项
  switch (snid) {
   case 1:
    Serial.print("1");
    break;
   case 2:
    Serial.print("2");
    break;
  }

}

void hardware_init(){
  //需要操作系统启动后初始化的内容
  setPinFun(13,SECOND_FUNCTION);
  setPinFun(14,SECOND_FUNCTION);
  Serial.begin(9600);
  while (1) {
    if(Serial.available() > 0){
      Rec = Serial.readString();
      if(Rec == "start"){
        delay(200);
        enter_wakeup(10000);
        delay(200);
        //{playid:10500,voice:欢迎使用智优购智能购物系统！请识别人脸进行登录！}
        play_audio(10500);
      }
      if(Rec == "open"){
        delay(200);
        enter_wakeup(10000);
        delay(200);
        //{playid:10501,voice:欢迎使用语音导航助手，请告诉我您需要购买什么？}
        play_audio(10501);
      }
      if(Rec == "login"){
        delay(200);
        enter_wakeup(10000);
        delay(200);
        //{playid:10502,voice:人脸登录成功！}
        play_audio(10502);
      }
    }
    delay(2);
  }
  vTaskDelete(NULL);
}

void setup()
{
  //音量范围1-7
  vol_set(4);
  //欢迎词指开机提示音，可以为空
  //{ID:1,keyword:"命令词",ASR:"薯片",ASRTO:"好的，这就带您去薯片柜台！"}
  //{ID:2,keyword:"命令词",ASR:"饮料",ASRTO:"好的，这就带您去饮料柜台！"}
}
