import tkinter as tk
import re
import tkinter.messagebox

from tkinter import ttk
from trend.trend import Trend
from PIL.ImageTk import PhotoImage

from utils.config import Config
from utils.non_image import NoneImage


class WindowMain(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.__config = Config()
        self.__URL_list = self.__config.get()
        self.__trend_ob = None
        self.__none_img = PhotoImage(image=NoneImage().get_none_img())
        # 弹窗界面
        self.__setup_ui()
        self.__init_text()

    def __setup_ui(self) -> None:
        self.title("设置")

        # 城市设置Frame
        edit_group = tk.LabelFrame(self, text="编辑区", padx=5, pady=5)
        add_button = tk.Button(edit_group, text="+", command=self.__add)
        add_button.grid(row=0, column=0)
        delete_button = tk.Button(edit_group, text="-", command=self.__delete)
        delete_button.grid(row=1, column=0)
        self.__URL_entry = tk.Entry(edit_group, width=61)
        self.__URL_entry.grid(row=0, column=1, columnspan=3)
        self.__alternative_box = tk.Listbox(edit_group,
                                            width=27,
                                            selectmode=tk.EXTENDED)
        self.__alternative_box.grid(row=1, column=1)
        in_out_frame = tk.Frame(edit_group)
        insert_button = tk.Button(in_out_frame,
                                  text=">>",
                                  command=self.__insert)
        insert_button.grid(row=0, column=0, pady=5)
        withdraw_button = tk.Button(in_out_frame,
                                    text="<<",
                                    command=self.__withdraw)
        withdraw_button.grid(row=1, column=0, pady=5)
        in_out_frame.grid(row=1, column=2)
        self.__select_box = tk.Listbox(edit_group,
                                       width=28,
                                       selectmode=tk.EXTENDED)
        self.__select_box.grid(row=1, column=3)
        edit_group.grid(row=0, column=0)

        analyse_buttom = tk.Button(self,
                                   text=">> 分析 >>",
                                   command=self.__analyse)
        analyse_buttom.grid(row=1, column=0, sticky=tk.EW)
        # 显示Frame
        view_frame = ttk.Notebook(self)
        view_frame.grid(row=3, column=0)
        cloud_img_frame = tk.Frame(view_frame)
        top_img_frame = tk.Frame(view_frame)

        cloud_img_frame.grid_rowconfigure(0, weight=1)
        cloud_img_frame.grid_columnconfigure(0, weight=1)
        top_img_frame.grid_rowconfigure(0, weight=1)
        top_img_frame.grid_columnconfigure(0, weight=1)

        self.__cloud_img_label = tk.Label(cloud_img_frame,
                                          image=self.__none_img)
        self.__cloud_img_label.grid(row=0, column=0, sticky=tk.NSEW)
        self.__top_img_label = tk.Label(top_img_frame, image=self.__none_img)
        self.__top_img_label.grid(row=0, column=0, sticky=tk.NSEW)

        view_frame.add(cloud_img_frame, text='词云图')
        view_frame.add(top_img_frame, text='词频分析')
        view_frame.grid(row=2, column=0, sticky=tk.NSEW)

    def __init_text(self) -> None:
        for item in self.__URL_list['URLs']['list']:
            self.__alternative_box.insert(tk.END, item)

    def __add(self):
        url_rules = re.compile('^(http(s)?:\/\/)\w+[^\s]+(\.[^\s]+){1,}$')
        URL_tmp = self.__URL_entry.get()
        if url_rules.fullmatch(URL_tmp) == None:
            tkinter.messagebox.showerror(title='错误', message='请输入正确的URL！')
            return
        list_tmp = self.__alternative_box.get(0, self.__alternative_box.size())
        list_tmp += self.__select_box.get(0, self.__select_box.size())
        if URL_tmp not in list_tmp:
            self.__alternative_box.insert(tk.END, URL_tmp)
        if URL_tmp not in self.__URL_list:
            self.__URL_list['URLs']['list'].append(URL_tmp)
            self.__config.update(self.__URL_list)
        self.__URL_entry.delete(0, tk.END)

    def __delete(self):
        delete_tmp = self.__alternative_box.curselection()
        delete_tmp_list = list(delete_tmp)
        delete_tmp_list.reverse()
        for index in delete_tmp_list:
            self.__URL_list['URLs']['list'].remove(
                self.__alternative_box.get(index))
            self.__alternative_box.delete(index)
        self.__config.update(self.__URL_list)

    def __analyse(self):
        if self.__select_box.size() == 0:
            return
        self.__fresh()

    def __fresh(self):
        URLs = self.__select_box.get(0, self.__select_box.size())
        self.__trend_ob = Trend(URLs)
        cloud_image, top_image = self.__trend_ob.get_img()

        self.__cloud_image = PhotoImage(cloud_image)
        self.__cloud_img_label.configure(image=self.__cloud_image)
        self.__top_image = PhotoImage(top_image)
        self.__top_img_label.configure(image=self.__top_image)

    def __insert(self):
        insert_tmp = self.__alternative_box.curselection()
        insert_tmp_list = list(insert_tmp)
        insert_tmp_list.reverse()
        for index in insert_tmp_list:
            self.__select_box.insert(tk.END, self.__alternative_box.get(index))
            self.__alternative_box.delete(index)

    def __withdraw(self):
        withdraw_tmp = self.__select_box.curselection()
        withdraw_tmp_list = list(withdraw_tmp)
        withdraw_tmp_list.reverse()
        for index in withdraw_tmp_list:
            self.__alternative_box.insert(tk.END, self.__select_box.get(index))
            self.__select_box.delete(index)
