from PIL import ImageTk, Image
import tkinter as tk
import helper as helper

'''
Points:

[L0_sella,
L1_nasion,
L2_porion,
L3_orbitale,
L4_ENP,
L5_ENA,
L6_point_A,
L7_point_B,
L8_pogonion,
L9_menton,
L10_gnathion,
L11_gonion,
L12_articulate,
L13_I1,
L14_I2,
L15_i1,
L16_i2,
L17_M1,
L18_M2,
L19_m1,
L20_m2]
'''

class Cephalo(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        self.pts = []
        self.pts_text = ["S","Na","Po","Or","ENP", "ENA","A","B","Pog","Me","Gn","Go",
                         "Ar","I1","I2","i_1","i_2","M1","M2","m_1","m_2"]

        self.angles_text = ["SNA","SNB","ANB","Â.Conv","Â.Facial","FMA","Â.Gon","Axe Y", "Etage Superieur",
                            "Etage Inferieur","I/F","i/m","I/i","alpha","beta"]

        self.canvas = tk.Canvas(self, width=1000, height=750, cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.img = ImageTk.PhotoImage(Image.open("cephalo_TM.jpg"))
        # self.img = ImageTk.PhotoImage(Image.open("cephalo_TM.jpg"))
        self.canvas.create_image(0, 0, image=self.img, anchor = 'nw')
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonPress-3>", self.on_back)


    def on_back(self, event):
        print(self.pts_text[len(self.pts)-1])
        self.canvas.delete(self.pts_text[len(self.pts)-1])
        self.canvas.delete(str(self.pts_text[len(self.pts)-1]) + "_pt")
        self.pts.pop(-1)


    def calculate(self):
        SNA = helper.get_angle(self.pts[0], self.pts[1], self.pts[6])
        SNB = helper.get_angle(self.pts[0], self.pts[1], self.pts[7])
        ANB = round(SNA - SNB)
        AC = round(180 - helper.get_angle(self.pts[8], self.pts[6], self.pts[1]))
        AF = helper.get_angle(self.pts[2], self.pts[3], self.pts[8])
        FMA = helper.get_angle_lines(self.pts[2], self.pts[3], self.pts[11], self.pts[9])
        AG = helper.get_angle(self.pts[9], self.pts[11], self.pts[12])
        AXE_Y = helper.get_angle_lines(self.pts[0], self.pts[10], self.pts[2], self.pts[3])
        E_SUP, E_INF = helper.rapport_etage(self.pts[5], self.pts[1], self.pts[9])
        I_F = helper.get_angle_lines(self.pts[13], self.pts[14], self.pts[2], self.pts[3])
        I_M = helper.get_angle_lines(self.pts[15], self.pts[16], self.pts[11], self.pts[9])


        self.angles = [SNA, SNB, ANB, AC, AF, FMA, AG, AXE_Y, E_SUP, E_INF, I_F, I_M]

        for i, angle in enumerate(self.angles):
            self.canvas.create_text(120, 20*i+500, fill="black", font="Times 12 bold",
                                    text=self.angles_text[i] + ": " + str(angle))

    # def calculate(self):
    #
    #     etage_sup, etage_inf = helper.rapport_etage(self.pts[0], self.pts[1], self.pts[2])
    #     self.canvas.create_text(120, 20*1+500, fill="black", font="Times 12 bold",
    #                             text=str(etage_sup))



    def on_button_press(self, event):
        if len(self.pts) == 17:
            self.calculate()
        else:
            self.x = event.x
            self.y = event.y
            x0,y0 = (self.x-2, self.y-2)
            x1,y1 = (event.x+2, event.y+2)
            self.canvas.create_oval(x0,y0,x1,y1, fill="red", tag = str(self.pts_text[len(self.pts)])+"_pt")
            self.canvas.create_text(self.x, self.y - 12, fill="red", font="Times 12 bold",
                                    text=self.pts_text[len(self.pts)], tag = self.pts_text[len(self.pts)])
            self.pts.append([float(self.x), float(self.y)])

        # if len(self.pts) == 3:
        #     self.angle = helper.get_angle(self.pts[0], self.pts[1], self.pts[2])
        #     self.canvas.create_text(self.pts[1][0], self.pts[1][1]-12, fill="red", font="Times 12",
        #                              text=self.angle)

if __name__ == "__main__":
    app = Cephalo()
    app.mainloop()