
import re


class Music:
    '''
    卑微小组作业之拓展 ————Arduino板喇叭音乐生成函数(Tone_Maker)   /* Made By YKL */\n
    目前进度\n
    frequency   频率 升调，平调，降调  A 1 a\n
    duration    持续时间 一拍，半拍，四分拍 - . 1_\n
    delay_time  暂停时间 时间间隔 \n
    basic_time  基础时长 音乐急促（300）与缓慢（600）\n
    mixing      混音 是否有间隔,重复\n
    threading   多线程\n

'''

    # above
    music_part = []
    pin_need = "8"
    file_name = "music.ino"
    basic_time = 200
    program_head = "void setup() {\n\n}\n\nint pin_need = " + \
        pin_need + ";\n\nvoid loop()\n{\n"
    program_foot = "\n}"
    program_str = ""

    def __init__(self):
        '''
        init 初始化，还没想好写什么\n
        '''
        print("Initing...")
        print("OK")

    # frequency
    def frequency_change(frequency, frequency_init=1):
        '''
        frequency_change 函数 实现功能\n
        1.根据输入匹配音调\n
        2.现有三种音调更改 A~G为高音 1~7为平音 a~g为低音\n

        不处理混音(mixing_music)与节拍(duration)\n
        '''
        frequency_dic = {"0": 0, "1": 262, "2": 294, "3": 330,
                         "4": 349, "5": 392, "6": 440, "7": 494}
        if len(frequency) == 1:
            if frequency >= "A" and frequency <= "Z":
                frequency = chr(ord(frequency)-16)
                frequency_init = 2
            elif frequency >= "a" and frequency <= "z":
                frequency = chr(ord(frequency)-48)
                frequency_init = 0.5
            elif frequency >= "0" and frequency <= "9":
                pass
            else:
                return frequency
        else:
            return frequency
        fre_ans = int(frequency_dic[frequency]*frequency_init)
        return fre_ans

    def frequency_list_change(frequency_list):
        '''
        frequency_list_change 频率核对改变函数\n
        frequency_change 处理函数\n
        '''
        mp_temp = []
        for frequency_cell in frequency_list:
            mp_temp.append(Music.frequency_change(frequency=frequency_cell))
        Music.duration_list_change([mp_temp])
        return 0

    # duration
    def duration_list_change(duration_list):
        '''
        duration_list_change 节拍时间调节\n
        duration_change  分函数\n
        '''
        dup_temp = []
        for duration_cell in duration_list:
            dup_temp.append(Music.duration_change(duration_list=duration_cell))
        return dup_temp

    def duration_change(duration_list):
        '''
        duration_change 函数 实现功能\n
        1.定出每拍持续时间\n
        2.支持 4拍 (- - -) | 2拍 (-) | 3/2拍(.) | 半拍 (_)\n

        不处理休眠时间调配(delay_time)\n
        '''
        duration_temp = 0
        duration_list_one = []
        duration_list_two = []
        duration_dic = {"-": 1, ".": 1.5}
        duration_init_num = 0

        for duration in duration_list:
            if type(duration) == int or type(duration) == float:
                duration_temp = duration
                duration_list_one.append(duration)
                duration_list_two.append(int(1*Music.basic_time))
                pass
            else:
                if len(duration) == 1 and duration != "0":
                    duration_init_num += 1
                    duration_list_one.pop()
                    duration_list_one.append([duration_temp, 1])
                    duration_list_one.append([duration_temp, 1])
                    duration_list_two.append(
                        int(duration_dic[duration]*Music.basic_time))
                elif len(duration) == 2:
                    duration_temp = Music.frequency_change(duration[0])
                    duration_list_one.append(duration_temp)
                    duration_list_two.append(int(0.5*Music.basic_time))
        Music.delaytime_list_change([duration_list_one, duration_list_two])

    # delay_time
    def delaytime_list_change(dt_list):
        '''
        delaytime_list_change 用于调整休眠时间 休止符\n
        dt_change 分函数\n
        '''
        Music.dt_change(dt_list)
        return 0

    def dt_change(delay_time_list):
        '''
        dt_change 实现功能:\n
        1.根据现有时长自动调平间隔时长\n

        配合混音(mixing_music)\n
        '''
        delay_list = []
        pointer_delay = 0
        delay_init_pow = 1   # 是否空音
        for delay_time in delay_time_list[0]:
            if type(delay_time) != tuple:
                delay_list.append(
                    int(delay_time_list[1][pointer_delay]*delay_init_pow))
            else:
                delay_list.append(0)
            pointer_delay += 1
        Music.data_cleaner(
            [delay_time_list[0], delay_time_list[1], delay_list])
        return 0

    # Data cleaning
    def data_cleaner(uncleaned_list):
        '''
        data_cleaner 数据清洗 实现功能\n
        1.数据整合与清洗\n
        2.衔接函数生成(function_generation)\n
        ..........................................................................................\n
        清洗输出格式: frequency:duration|delaytime\n
        ..........................................................................................\n
        临时值(temp)说明\n
        temp_one:循环用全局计数器\n
        temp_two:寄存上级数据\n
        temp_three:多拍数据处理\n
        temp_four:结果传递\n
        '''

        temp_one = 0
        temp_two = 0
        temp_three = {}
        temp_four = ""
        for temp_one in range(len(uncleaned_list[0])):
            frequency_clean = uncleaned_list[0][temp_one]
            duration_clean = uncleaned_list[1][temp_one]
            delaytime_clean = uncleaned_list[2][temp_one]
            index_list = [duration_clean, delaytime_clean]
            if type(frequency_clean) == int and frequency_clean != 0:
                if temp_three != {}:
                    Music.data_intergration("{}:{}|{}".format([i for i in temp_three][0], [
                        temp_three[i][0] for i in temp_three][0], [temp_three[i][1] for i in temp_three][0]))
                    temp_three = {}
                Music.data_intergration("{}:{}|{}".format(frequency_clean,
                                                          duration_clean, delaytime_clean))

            elif type(frequency_clean) == list:
                if temp_three == {}:
                    temp_three[frequency_clean[0]] = [
                        duration_clean, delaytime_clean]

                elif frequency_clean[0] in temp_three:
                    for temp_two in range(len(temp_three[frequency_clean[0]])):
                        temp_three[frequency_clean[0]
                                   ][temp_two] += index_list[temp_two]

            elif frequency_clean == 0:
                if temp_three != {}:
                    Music.data_intergration("{}:{}|{}".format([i for i in temp_three][0], [
                        temp_three[i][0] for i in temp_three][0], [temp_three[i][1] for i in temp_three][0]))
                    temp_three = {}
                Music.data_intergration(delaytime=delaytime_clean)

            temp_one += 1

        if temp_three != {}:
            Music.data_intergration("{}:{}|{}".format([i for i in temp_three][0], [
                temp_three[i][0] for i in temp_three][0], [temp_three[i][1] for i in temp_three][0]))
            temp_three = {}

    def data_intergration(data="", delaytime=None):
        """
        data_intergration 数据整合 实现功能\n
        1.进一步整合数据,并写入文档\n
        2.联系数据清洗(data_cleaner),进一步处理数据\n
        """
        global program_str
        if data != "" and delaytime == None:
            frequency, duration, delay = re.split("[:|]", data)
            Music.program_str += 'tone(pin_need , {} , {} );\n delay( {} );\n'.format(
                frequency, duration, delay)
        else:
            Music.program_str += "delay( {} );\n".format(delaytime)
        return Music.program_str

    def data_write(file, program, program_head=program_head, program_foot=program_foot):
        """
        data_write 程序写入 实现功能\n
        1.将程序写入文件\n
        """
        file_open = open(file, "w", encoding="utf-8")
        file_open.writelines(program_head + program + program_foot)
        file_open.close()

    # Others

    def mixing_music():
        '''
        mixing_music 混音处理函数 实现功能\n
        1.实现重复(| ... |)\n
        2.实现连音(( ... ))\n
        '''

        return 0

    def arduino_threading():
        '''
        arduino_threading 函数多线程模块 实现功能\n
        1.多线程实现函数循环\n
        '''
        threading_time = 0
        return 0
