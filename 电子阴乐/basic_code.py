

from music_init import Music as music

if __name__ == "__main__":

    doc_music = input("输入音阶或导入音乐文本(文本请用txt格式):")
    if ".txt" in doc_music:
        music_file = open(doc_music, "r", encoding="utf-8")
        for music_cell in music_file.readlines():
            # print(music_cell.split("\n")[0].split(" "))
            music_cell = music.frequency_list_change(
                frequency_list=music_cell.split("\n")[0].split(" "))
        # print(music.program_str)
        music.data_write(file= music.file_name,program = music.program_str)
    else:
        print("不支持...")
    # print(music.music_part)
