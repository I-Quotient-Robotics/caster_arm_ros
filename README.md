# Caster-ARM

Caster-ARM移动抓取平台ROS包

## 前期准备

1. 参考《Caster用户手册》，完成Caster的检查和硬件启动
2. 参考KINOVA JACO2 Gen2的使用说明，完成机械臂的检查和启动
3. 确保Caster和机械臂的活动范围内无异物
4. 确保Caster正前方区域没有杂物或者与地面颜色不一致的物体

## 使用流程

1. 在终端中输入如下指令，启动Caster-ARM的ROS驱动部分

   ```bash
   roslaunch caster_arm_base bringup_all.launch
   ```

2. 等待上面的指令执行完成，且没有报错后，开启新的终端，输入如下指令，打开rviz

   ```bash
   roslaunch caster_arm_viz display.launch
   ```

3. 在rviz中，用户可以观察到机械臂的模型与真机一致，腕部相机的画面也会显示在rviz中
4. 请参考[CasterUserManual](https://github.com/CasterLab/caster_user_manual/blob/master/zh_cn/quick_start.md#%E6%89%8B%E6%9F%84%E6%8E%A7%E5%88%B6)手柄控制的章节，使用手柄控制Caster的运动

## 物体识别与抓取示例

1. 在完成[使用流程](使用流程)中的第一步后，执行如下指令，启动MoveIt

   ```bash
   roslaunch caster_arm_moveit_config execute.launch
   ```

2. 等待上述程序启动完成后，用户可以在rviz中看到机械臂的MoveIt操控组件。可以通过手动拖拽界面控件的方式，控制真机进行运动

3. 将Caster和机械臂活动范围内的杂物清空，然后在Caster的正前方地面上（距离Caster前端10-60cm，宽度50cm的范围内）放置一个装有水的，有标签纸的水瓶。水瓶底朝向Caster前端。

4. 在新的窗口中启动下面的指令

   ```bash
   roslaunch caster_arm_app pick_place_demo.launch
   ```

5. 当指令正确启动后，机械臂会抓起Caster面前的瓶子，然后举到空中，此时用户要用手抓住机械爪手中的瓶子，避免砸到其它物品
6. 程序会反复执行第五步中的步骤，直到用户关闭程序

## 定位导航

参考[CasterUserManual](https://github.com/CasterLab/caster_user_manual#user-manual)中创建地图与定位导航章节

## 自动充电功能

参考[CasterUserManual](https://github.com/CasterLab/caster_user_manual/blob/master/zh_cn/quick_start.md#%E8%87%AA%E5%8A%A8%E5%85%85%E7%94%B5%E5%8A%9F%E8%83%BD)中自动充电功能章节

**注意：自动充电功能需要先建立地图，且仍处于pre-release阶段，请谨慎使用**


