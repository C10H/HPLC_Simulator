"""
copyleft:C10H15N
色谱图线模拟器
已知柱效等求出色谱图线
目前适用于分析型色谱（进样时间可忽略）和制备型色谱（进样时间不可忽略）
适用于线性情况及非线性情况,非线性情况包括BET公式,Toth公式及朗格缪尔公式
单样品进样及Bi-Langmuir手性拆分多样品进样
------------------------
main.py
在本色谱程序中负责前端交互
采用tkinter,布局统一采用place,anchor基本采用NW
by C10H15N
2021.8.8
"""
from tkinter import *
import linear  # 详细内容请见linear.py
import Langmuir  # 详细内容请见Langmuir.py
import Toth  # 详细内容请见Toth.py
import BET  # 详细内容请见BET.py
import nonlinear  # 详细内容请见nonlinear.py
import BiLangmuir  # 详细内容请见BiLangmuir.py
from tkinter.filedialog import *
from tkinter import messagebox


class GUI():
    def __init__(self, root):
        self.initGUI(root)

    def initGUI(self, root):
        def go():

            for l in L:
                l.place_forget()
            for enter in Enter:
                enter.place_forget()

            if v.get() == 2:  # 线性
                L[0].place(relx=0, rely=0.6, anchor='nw')
                Enter[0].place(relx=0.2, rely=0.6, anchor='nw')
            elif v.get() == 3:  # Langmuir
                L[1].place(relx=0, rely=0.6, anchor='nw')
                Enter[1].place(relx=0.2, rely=0.6, anchor='nw')  # qs
                L[2].place(relx=0, rely=0.65, anchor='nw')
                Enter[2].place(relx=0.2, rely=0.65, anchor='nw')  # b
            elif v.get() == 4:  # Toth
                L[3].place(relx=0, rely=0.6, anchor='nw')
                Enter[3].place(relx=0.2, rely=0.6, anchor='nw')  # vl
                L[4].place(relx=0, rely=0.65, anchor='nw')
                Enter[4].place(relx=0.2, rely=0.65, anchor='nw')  # b
                L[5].place(relx=0, rely=0.7, anchor='nw')
                Enter[5].place(relx=0.2, rely=0.7, anchor='nw')  # n
            elif v.get() == 5:  # BET
                L[6].place(relx=0, rely=0.6, anchor='nw')
                Enter[6].place(relx=0.2, rely=0.6, anchor='nw')  # q0
                L[7].place(relx=0, rely=0.65, anchor='nw')
                Enter[7].place(relx=0.2, rely=0.65, anchor='nw')  # p0
                L[8].place(relx=0, rely=0.7, anchor='nw')
                Enter[8].place(relx=0.2, rely=0.7, anchor='nw')  # c
            elif v.get() == 6:  # Bi-Langmuir
                L[9].place(relx=0, rely=0.6, anchor='nw')
                Enter[9].place(relx=0.2, rely=0.6, anchor='nw')  # q0
                L[10].place(relx=0, rely=0.65, anchor='nw')
                Enter[10].place(relx=0.2, rely=0.65, anchor='nw')  # p0
                L[11].place(relx=0, rely=0.7, anchor='nw')
                Enter[11].place(relx=0.2, rely=0.7, anchor='nw')  # c
                L[12].place(relx=0.5, rely=0.6, anchor='nw')
                Enter[12].place(relx=0.7, rely=0.6, anchor='nw')  # q0
                L[13].place(relx=0.5, rely=0.65, anchor='nw')
                Enter[13].place(relx=0.7, rely=0.65, anchor='nw')  # p0
                L[14].place(relx=0.5, rely=0.7, anchor='nw')
                Enter[14].place(relx=0.7, rely=0.7, anchor='nw')  # c
            # elif v.get() == 7:  # 其他非线性
            #     L[15].place(relx=0, rely=0.6, anchor='nw')
            #     Enter[15].place(relx=0.2, rely=0.6, anchor='nw')  # 吸附表
            return

        def fileSave():
            filenewpath = asksaveasfilename(defaultextension='png')
            filenewname.set(filenewpath)

        def onClick():
            try:
                int(theoretical_plate_number.get())
            except:
                messagebox.showerror("理论塔板数请输入整数")
            try:
                float(column_length.get())
            except:
                messagebox.showerror("柱管长度请输入实数")
            try:
                float(column_diameter.get())
            except:
                messagebox.showerror("柱管直径请输入实数")
            try:
                float(flow.get())
            except:
                messagebox.showerror("流速请输入实数")
            try:
                float(dead_time.get())
            except:
                messagebox.showerror("死时间请输入实数")
            try:
                float(inject_volume.get())
            except:
                messagebox.showerror("柱管体积请输入实数")
            try:
                float(duration.get())
            except:
                messagebox.showerror("模拟时间请输入实数")
            if v.get() == 2:  # 线性
                linear.Linear(
                    theoretical_plate_number=int(theoretical_plate_number.get()),
                    column_length=float(column_length.get()),
                    column_diameter=float(column_diameter.get()),
                    flow=float(flow.get()),
                    dead_time=float(dead_time.get()),
                    inject_time=float(inject_time.get()),
                    inject_volume=float(inject_volume.get()),
                    duration=float(duration.get()),
                    k=float(k.get()),
                    savepath=filenewname.get()
                )
            elif v.get() == 3:  # langmuir
                sheet = {'x': Langmuir.langmuir(float(qs.get()), float(b.get())).x,
                         'y': Langmuir.langmuir(float(qs.get()), float(b.get())).y}
                nonlinear.Nonlinear(
                    theoretical_plate_number=int(theoretical_plate_number.get()),
                    column_length=float(column_length.get()),
                    column_diameter=float(column_diameter.get()),
                    flow=float(flow.get()),
                    dead_time=float(dead_time.get()),
                    inject_time=float(inject_time.get()),
                    inject_volume=float(inject_volume.get()),
                    duration=float(duration.get()),
                    sheet=sheet,
                    savepath=filenewname.get()
                )
            elif v.get() == 4:
                sheet = {'x': Toth.toth(float(VL.get()), float(Toth_b.get()), float(n.get())).x,
                         'y': Toth.toth(float(VL.get()), float(Toth_b.get()), float(n.get())).y}
                nonlinear.Nonlinear(
                    theoretical_plate_number=int(theoretical_plate_number.get()),
                    column_length=float(column_length.get()),
                    column_diameter=float(column_diameter.get()),
                    flow=float(flow.get()),
                    dead_time=float(dead_time.get()),
                    inject_time=float(inject_time.get()),
                    inject_volume=float(inject_volume.get()),
                    duration=float(duration.get()),
                    sheet=sheet,
                    savepath=filenewname.get()
                )
            elif v.get() == 5:  # BET
                sheet = {'x': BET.BET(float(q0.get()), float(p0.get()), float(c.get())).x,
                         'y': BET.BET(float(q0.get()), float(p0.get()), float(c.get())).y}
                nonlinear.Nonlinear(
                    theoretical_plate_number=int(theoretical_plate_number.get()),
                    column_length=float(column_length.get()),
                    column_diameter=float(column_diameter.get()),
                    flow=float(flow.get()),
                    dead_time=float(dead_time.get()),
                    inject_time=float(inject_time.get()),
                    inject_volume=float(inject_volume.get()),
                    duration=float(duration.get()),
                    sheet=sheet,
                    savepath=filenewname.get()
                )
            elif v.get() == 6:  # 双朗格缪尔手性吸附
                BiLangmuir.BiLangmuir(
                    qns=float(qns.get()), kns=float(kns.get()), qs1=float(qs1.get()),
                    ks1=float(ks1.get()), qs2=float(qs2.get()), ks2=float(ks2.get()),
                    theoretical_plate_number=int(theoretical_plate_number.get()),
                    column_length=float(column_length.get()),
                    column_diameter=float(column_diameter.get()),
                    flow=float(flow.get()),
                    dead_time=float(dead_time.get()),
                    inject_time=float(inject_time.get()),
                    inject_volume=float(inject_volume.get()),
                    duration=float(duration.get()),
                    savepath=filenewname.get()
                )
            elif v.get() == 7:  # 其他非线性
                pass
            messagebox.showinfo("图像已保存")

        theoretical_plate_number = StringVar()
        column_length = StringVar()
        column_diameter = StringVar()
        flow = StringVar()
        dead_time = StringVar()
        inject_time = StringVar()
        inject_volume = StringVar()
        duration = StringVar()

        root.title("色谱图线模拟--参数输入")
        root.geometry('800x600+200+55')

        Label(root,
              text="欢迎使用色谱图线模拟程序,请输入色谱柱的参数",
              font=("Arial Bold", 12)).place(relx=0, rely=0, anchor='nw')
        Label(root,
              text="理论塔板数",
              font=("Arial Bold", 12)).place(relx=0, rely=0.05, anchor='nw')

        Entry(root, width=25, textvariable=theoretical_plate_number).place(relx=0.4, rely=0.05, anchor='nw')
        Label(root, text="柱管长度(cm)", font=("Arial Bold", 12)).place(relx=0, rely=0.1, anchor='nw')
        Entry(root, width=25, textvariable=column_length).place(relx=0.4, rely=0.1, anchor='nw')
        Label(root, text="柱管直径(mm)", font=("Arial Bold", 12)).place(relx=0, rely=0.15, anchor='nw')
        Entry(root, width=25, textvariable=column_diameter).place(relx=0.4, rely=0.15, anchor='nw')
        Label(root, text="流速(ml/min)", font=("Arial Bold", 12)).place(relx=0, rely=0.2, anchor='nw')
        Entry(root, width=25, textvariable=flow).place(relx=0.4, rely=0.2, anchor='nw')
        Label(root, text="死时间(min)", font=("Arial Bold", 12)).place(relx=0, rely=0.25, anchor='nw')
        Entry(root, width=25, textvariable=dead_time).place(relx=0.4, rely=0.25, anchor='nw')
        Label(root, text="进样时间(min)", font=("Arial Bold", 12)).place(relx=0, rely=0.3, anchor='nw')
        Entry(root, width=25, textvariable=inject_time).place(relx=0.4, rely=0.3, anchor='nw')
        Label(root, text="进样量", font=("Arial Bold", 12)).place(relx=0, rely=0.35, anchor='nw')
        Entry(root, width=25, textvariable=inject_volume).place(relx=0.4, rely=0.35, anchor='nw')
        Label(root, text="模拟时长", font=("Arial Bold", 12)).place(relx=0, rely=0.4, anchor='nw')
        Entry(root, width=25, textvariable=duration).place(relx=0.4, rely=0.4, anchor='nw')
        Label(root, text="吸附曲线类型", font=("Arial Bold", 12)).place(relx=0, rely=0.45, anchor='nw')

        v = IntVar()
        v.set(1)
        MODES = [
            ('请选择', 1),
            ('线性(y=kx)', 2),
            ('朗格缪尔(qs,b)', 3),
            ('Toth(VL,b,n)', 4),
            ('BET(q0,p0,c)', 5),
            ('双Langmuir手性拆分(qns,kns,qs1,ks1,qs2,ks2)', 6)
            # ('其他非线性', 7)
        ]
        for mode, num in MODES:
            if num <= 4:
                b = Radiobutton(root, text=mode, variable=v, value=num, command=go)
                b.place(relx=(num - 1) * 0.25, rely=0.5, anchor='nw')
            elif num <= 6:
                b = Radiobutton(root, text=mode, variable=v, value=num, command=go)
                b.place(relx=(num - 5) * 0.25, rely=0.55, anchor='nw')
            else:
                b = Radiobutton(root, text=mode, variable=v, value=num, command=go)
                b.place(relx=0.75, rely=0.55, anchor='nw')

        L = []
        Enter = []
        # 线性吸附参数 0
        k = StringVar()
        L.append(Label(root, text="k", font=("Arial Bold", 12)))
        Enter.append(Entry(root, width=25, textvariable=k))
        # 朗格缪尔吸附参数 12
        qs = StringVar()
        b = StringVar()
        L.append(Label(root, text="qs", font=("Arial Bold", 12)))
        Enter.append(Entry(root, width=25, textvariable=qs))
        L.append(Label(root, text="b", font=("Arial Bold", 12)))
        Enter.append(Entry(root, width=25, textvariable=b))
        # Toth吸附常数 345
        VL = StringVar()
        Toth_b = StringVar()
        n = StringVar()
        L.append(Label(root, text="VL", font=("Arial Bold", 12)))
        Enter.append(Entry(root, width=25, textvariable=VL))
        L.append(Label(root, text="b", font=("Arial Bold", 12)))
        Enter.append(Entry(root, width=25, textvariable=Toth_b))
        L.append(Label(root, text="n", font=("Arial Bold", 12)))
        Enter.append(Entry(root, width=25, textvariable=n))
        # BET吸附常数 678
        q0 = StringVar()
        p0 = StringVar()
        c = StringVar()
        L.append(Label(root, text="q0", font=("Arial Bold", 12)))
        Enter.append(Entry(root, width=25, textvariable=q0))
        L.append(Label(root, text="p0", font=("Arial Bold", 12)))
        Enter.append(Entry(root, width=25, textvariable=p0))
        L.append(Label(root, text="c", font=("Arial Bold", 12)))
        Enter.append(Entry(root, width=25, textvariable=c))
        # 双朗格缪尔手性拆分 9abcde
        qns = StringVar()
        kns = StringVar()
        qs1 = StringVar()
        ks1 = StringVar()
        qs2 = StringVar()
        ks2 = StringVar()
        L.append(Label(root, text="qns", font=("Arial Bold", 12)))
        Enter.append(Entry(root, width=25, textvariable=qns))
        L.append(Label(root, text="kns", font=("Arial Bold", 12)))
        Enter.append(Entry(root, width=25, textvariable=kns))
        L.append(Label(root, text="qs1", font=("Arial Bold", 12)))
        Enter.append(Entry(root, width=25, textvariable=qs1))
        L.append(Label(root, text="ks1", font=("Arial Bold", 12)))
        Enter.append(Entry(root, width=25, textvariable=ks1))
        L.append(Label(root, text="qs2", font=("Arial Bold", 12)))
        Enter.append(Entry(root, width=25, textvariable=qs2))
        L.append(Label(root, text="ks2", font=("Arial Bold", 12)))
        Enter.append(Entry(root, width=25, textvariable=ks2))
        # 其他非线性 10
        # L.append(Label(root, text="吸附数据", font=("Arial Bold", 12)))
        # Enter.append(Entry(root, width=25))

        # 选择色谱图保存位置
        filenewname = StringVar()
        Entry(root, width=25, textvariable=filenewname).place(relx=0.4, rely=0.75, anchor='nw')
        Label(root, text="色谱图线保持位置", font=("Arial Bold", 12)).place(relx=0, rely=0.75, anchor='nw')
        Button(root, text="点击选择", command=fileSave).place(relx=0.8, rely=0.75, anchor='nw')
        Button(root, text='submit', font=("Arial Bold", 12), command=onClick).place(relx=0.5, rely=0.85,
                                                                                    anchor='c')

        root.mainloop()


if __name__ == '__main__':
    root = Tk()
    myGUI = GUI(root)
