#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import os
import time
import datetime
import subprocess
import parameters as para
from sensing import Sensor
from emr_gen import Emr_gen


senser = Sensor()
gen = Emr_gen()


class Emr_rec:
    def __init__(self):
        self.res = para.res
        self.thd = para.thd
        self.ratio = para.ratio
        self.resos = para.resos
        self.interval = para.interval
        self.end_interval = para.end_interval
        self.output_dirpath = './tmp/'
        self.emr_dirpath = './emr/'
        self.cam_No = 'emr_' + para.PREFIX_IN + '_'  
        self.trigger_select = para.TRIGGER_SELECT

        # directory for saving
        os.makedirs(self.output_dirpath, exist_ok=True)
        os.makedirs(self.emr_dirpath, exist_ok=True)

        for i in range(5):
            if self.res == i: 
                self.width = self.resos[i][0]
                self.heigth = self.resos[i][1]
                self.label_pos = self.resos[i][2]
                self.fps = self.resos[i][3]
                self.f_size = self.resos[i][4]
                self.chd_pix = self.resos[i][0] * self.resos[i][1] * self.ratio
                break

        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')#('M','J','P','G')


    def exec(self):
        #映像入力用のvideoCapture 作成
        device_id = -1
        self.cap = cv2.VideoCapture(device_id)

        #Cameraをオープンできなかったらreboot
        if True==self.cap.isOpened(): 
            self.cap.set(3, self.width)
            self.cap.set(4, self.heigth)
            self.cap.set(5, self.fps)
        else:
            time.sleep(90)
            subprocess.call(["sudo","reboot"])

        #録画関数呼び出し
        while True:
            self.set_loop()

            # q キーを押したら終了する。 
            if cv2.waitKey(1) == 13:
                self.cap.release()
                cv2.destroyAllWindows()
        

    #長さ4秒の動画を01.aviから05.aviまで5本録画してたら01.aviから順に上書きするループ関数
    def set_loop(self):
        emr_trigger = 0

        for loop_count in (range(5)):
            file_name = '0' + str(loop_count+1)

            writer = cv2.VideoWriter(self.output_dirpath + file_name + '.mp4', self.fourcc, self.fps, (self.width, self.heigth))

            if self.trigger_select == 0:
                emr_trigger = self.video_writer_sensor(emr_trigger, writer) #センサーtrigger時はこちらをアンコメント
            elif self.trigger_select == 1:
                emr_trigger = self.video_writer_diff(emr_trigger, writer) #image差分動体検知trigger時はこちらをアンコメント

            if emr_trigger ==1: #直前の録画ループ中にセンサーが検知してたら、録画後にtmpフォルダーの動画を結合する
                if loop_count == 4: file_name = '01'
                else: file_name = '0' + str(loop_count+2)

                writer = cv2.VideoWriter(self.output_dirpath + file_name + '.mp4', self.fourcc, self.fps, (self.width, self.heigth))

                if self.trigger_select == 0:
                    emr_trigger = self.video_writer_sensor(emr_trigger, writer) #センサーtrigger時はこちらをアンコメント
                elif self.trigger_select == 1:
                    emr_trigger = self.video_writer_diff(emr_trigger, writer) #image差分動体検知trigger時はこちらをアンコメント

                emr_filename = self.cam_No + datetime.datetime.now().strftime('%Y%m%d%H%M')
                gen.combine_file(emr_filename, self.width, self.heigth, self.fps)
                emr_trigger = 0
                writer.release()
                return

            if cv2.waitKey(1) == (13):
                self.cap.release()
                cv2.destroyAllWindows()
                return True  # q キーを押したら終了する。


    #image差分動体検知triggerでEvent検知する録画書込みルーチン
    def video_writer_diff(self, emr_trigger, writer):
        trigger_change = 0
        
        t0=datetime.datetime.now()
        t1=datetime.datetime.now()
        delta = t1 - t0
        
        if emr_trigger == 1: interval = self.end_interval
        else: interval = self.interval

        while delta <= interval:

            _, frame = self.cap.read() # 1フレームずつ取得する            
            _, frame2 = self.cap.read()
            _, frame3 = self.cap.read()
            #if not ret:
            #    return  # 映像取得に失敗

            cv2.putText(frame, t1.strftime('%Y/%m/%d/%H:%M:%S'), (0, self.label_pos), cv2.FONT_HERSHEY_COMPLEX_SMALL, self.f_size, (255, 255, 255), 1, cv2.LINE_AA) #self.label_pos
            writer.write(frame)
            cv2.putText(frame2, t1.strftime('%Y/%m/%d/%H:%M:%S'), (0, self.label_pos), cv2.FONT_HERSHEY_COMPLEX_SMALL, self.f_size, (255, 255, 255), 1, cv2.LINE_AA)
            writer.write(frame2)
            cv2.putText(frame3, t1.strftime('%Y/%m/%d/%H:%M:%S'), (0, self.label_pos), cv2.FONT_HERSHEY_COMPLEX_SMALL, self.f_size, (255, 255, 255), 1, cv2.LINE_AA)
            writer.write(frame3)

            #if ret and ret2 and ret3:
            #グレースケールに変換
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            gray3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)
    
            diff1 = cv2.absdiff(gray2,gray)
            diff2 = cv2.absdiff(gray3,gray2)

            diff_and = cv2.bitwise_and(diff1, diff2)

            th = cv2.threshold(diff_and, self.thd, 255, cv2.THRESH_BINARY)[1]

            if cv2.countNonZero(th) > self.chd_pix:
                trigger_change = 1

            t1=datetime.datetime.now()
            delta = t1 - t0

        if trigger_change == 1: emr_trigger = 1

        writer.release()

        return emr_trigger


    #近接/人感センサーtriggerでEvent検知する録画書込みルーチン
    def video_writer_sensor(self, emr_trigger, writer):
        trigger_change = 0
        
        t0=datetime.datetime.now()
        t1=datetime.datetime.now()
        delta = t1 - t0
        
        if emr_trigger == 1: interval = self.end_interval
        else: interval = self.interval

        while delta <= interval:
            ret, frame = self.cap.read() # 1フレームずつ取得する
            #if not ret:
            #    return  # 映像取得に失敗
            cv2.putText(frame, t1.strftime('%Y/%m/%d/%H:%M:%S'), (0, self.label_pos), cv2.FONT_HERSHEY_COMPLEX_SMALL, self.f_size, (255, 255, 255), 1, cv2.LINE_AA)
            #cv2.imshow('frame', frame) #モニター表示はコメントアウト
            writer.write(frame)  # フレームを書き込む。
            t1=datetime.datetime.now()
            delta = t1 - t0
            tr_signal = senser.detect_counter() # センサーの物体検知有無を確認
            if tr_signal == 1: 
                trigger_change = 1 #センサーが検知した場合に返り値1を戻すためのフラグを立てる
            
            if cv2.waitKey(1) & 0xFF == ord('q'):break  # q キーを押したら終了する。

        if trigger_change == 1: emr_trigger = 1

        writer.release()

        return emr_trigger

if __name__ == '__main__':
    time.sleep(10)
    
    rec = Emr_rec()
    rec.exec()
