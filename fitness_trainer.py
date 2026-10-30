import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from pathlib import Path
from datetime import date, timedelta

BASE=Path.home()/"FitnessTrainerMAX"
BASE.mkdir(exist_ok=True)
db=sqlite3.connect(BASE/"fitness_trainer.db")
db.execute("CREATE TABLE IF NOT EXISTS workouts(id INTEGER PRIMARY KEY,day TEXT,activity TEXT,minutes INTEGER,note TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS meals(id INTEGER PRIMARY KEY,day TEXT,meal TEXT,description TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS goals(id INTEGER PRIMARY KEY,day TEXT,achievement TEXT)")
db.commit()

BG="#080D11"; SIDE="#0C1419"; PANEL="#111C22"; PANEL2="#15262B"
GREEN="#19F59B"; WHITE="#F3FAF8"; MUTED="#829A9A"; BORDER="#24413C"
FONT="Segoe UI"

root=tk.Tk()
root.title("FITNESS TRAINER MAX  |  Neon Edition")
root.geometry("1190x780")
root.minsize(960,650)
root.configure(bg=BG)
style=ttk.Style(root)
style.theme_use("clam")
style.configure("Neon.Treeview",background=PANEL,foreground=WHITE,fieldbackground=PANEL,
                borderwidth=0,rowheight=34,font=(FONT,10))
style.configure("Neon.Treeview.Heading",background=PANEL2,foreground=GREEN,
                relief="flat",font=(FONT,10,"bold"))
style.map("Neon.Treeview",background=[("selected","#1A5749")],foreground=[("selected",WHITE)])

def text(parent,value,size=11,color=WHITE,bold=False,bg=None,**kw):
    return tk.Label(parent,text=value,fg=color,bg=bg or parent.cget("bg"),
                    font=(FONT,size,"bold" if bold else "normal"),**kw)
def panel(parent,padx=22,pady=20):
    f=tk.Frame(parent,bg=PANEL,highlightbackground=BORDER,highlightthickness=1)
    f.pack(fill="x",padx=0,pady=(0,14))
    inner=tk.Frame(f,bg=PANEL)
    inner.pack(fill="both",expand=True,padx=padx,pady=pady)
    return inner
def button(parent,title,command,accent=True):
    b=tk.Button(parent,text=title,command=command,fg=BG if accent else GREEN,
                bg=GREEN if accent else PANEL2,activebackground="#69FFC1",
                activeforeground=BG,bd=0,relief="flat",cursor="hand2",
                font=(FONT,10,"bold"),padx=19,pady=11)
    return b
def entry(parent,hint):
    text(parent,hint,10,MUTED,bg=PANEL).pack(anchor="w",pady=(10,5))
    e=tk.Entry(parent,bg=PANEL2,fg=WHITE,insertbackground=GREEN,
               font=(FONT,11),relief="flat",highlightthickness=1,
               highlightbackground=BORDER,highlightcolor=GREEN)
    e.pack(fill="x",ipady=10)
    return e
def table(parent,cols):
    holder=tk.Frame(parent,bg=PANEL)
    holder.pack(fill="both",expand=True,pady=(10,0))
    tree=ttk.Treeview(holder,columns=cols,show="headings",height=8,style="Neon.Treeview")
    for c in cols:
        tree.heading(c,text=c)
        tree.column(c,width=150,stretch=True)
    bar=ttk.Scrollbar(holder,orient="vertical",command=tree.yview)
    tree.configure(yscrollcommand=bar.set)
    tree.pack(side="left",fill="both",expand=True)
    bar.pack(side="right",fill="y")
    return tree
def update_table(tree,sql):
    tree.delete(*tree.get_children())
    for item in db.execute(sql): tree.insert("",tk.END,values=item)

shell=tk.Frame(root,bg=BG)
shell.pack(fill="both",expand=True)
sidebar=tk.Frame(shell,bg=SIDE,width=245)
sidebar.pack(side="left",fill="y")
sidebar.pack_propagate(False)
main=tk.Frame(shell,bg=BG)
main.pack(side="left",fill="both",expand=True)
text(sidebar,"◉  FITNESS",19,GREEN,True,bg=SIDE).pack(anchor="w",padx=25,pady=(33,0))
text(sidebar,"     TRAINER MAX",12,WHITE,True,bg=SIDE).pack(anchor="w",padx=25,pady=(0,34))
text(sidebar,"МЕНЮ",9,MUTED,True,bg=SIDE).pack(anchor="w",padx=25,pady=(0,12))
nav={}
pages={}
items=[("home","⌂","Главная"),("work","▣","Тренировки"),
       ("food","◈","Питание"),("progress","▥","Прогресс"),
       ("achieve","★","Достижения"),("coach","✦","Помощник")]
header=tk.Frame(main,bg=BG)
header.pack(fill="x",padx=34,pady=(25,13))
title=text(header,"",23,WHITE,True)
title.pack(anchor="w")
subtitle=text(header,"",10,MUTED)
subtitle.pack(anchor="w",pady=(5,0))
body=tk.Frame(main,bg=BG)
body.pack(fill="both",expand=True,padx=34,pady=(0,20))
for key,icon,name in items:
    outer=tk.Frame(body,bg=BG)
    pages[key]=outer
def show(key):
    for p in pages.values():p.pack_forget()
    pages[key].pack(fill="both",expand=True)
    title.config(text=dict((a,c) for a,b,c in items)[key])
    subtitles={"home":"Твой день. Твой темп. Твой прогресс.",
               "work":"Записывай активность и отмечай свои тренировки.",
               "food":"Простой дневник питания без подсчёта калорий.",
               "progress":"Наблюдай за своей активностью с течением времени.",
               "achieve":"Отмечай важные личные победы.",
               "coach":"Общие советы по тренировкам и восстановлению."}
    subtitle.config(text=subtitles[key])
    for k,b in nav.items():
        b.configure(bg=PANEL2 if k==key else SIDE,fg=GREEN if k==key else MUTED)
    refresh()
for key,icon,name in items:
    b=tk.Button(sidebar,text=f"  {icon}    {name}",anchor="w",bd=0,relief="flat",
                font=(FONT,11,"bold"),bg=SIDE,fg=MUTED,activebackground=PANEL2,
                activeforeground=GREEN,cursor="hand2",padx=21,pady=16,
                command=lambda k=key:show(k))
    b.pack(fill="x",padx=10,pady=2)
    nav[key]=b
tk.Frame(sidebar,bg=SIDE).pack(expand=True,fill="both")
text(sidebar,"●  LOCAL MODE",10,GREEN,True,bg=SIDE).pack(anchor="w",padx=24,pady=(0,5))
text(sidebar,"Данные сохраняются на ПК",9,MUTED,bg=SIDE).pack(anchor="w",padx=24,pady=(0,24))

# Home
h=pages["home"]
hero=panel(h,padx=26,pady=24)
text(hero,"WELCOME BACK",10,GREEN,True,bg=PANEL).pack(anchor="w")
text(hero,"Продолжай двигаться вперёд",23,WHITE,True,bg=PANEL).pack(anchor="w",pady=(8,4))
text(hero,"Регулярность важнее идеального результата.",11,MUTED,bg=PANEL).pack(anchor="w")
button(hero,"+  Записать тренировку",lambda:show("work")).pack(anchor="w",pady=(18,0))
statrow=tk.Frame(h,bg=BG)
statrow.pack(fill="x",pady=(2,14))
stat_labels=[]
for i,(heading,unit) in enumerate([("ТРЕНИРОВКИ","всего"),("АКТИВНОСТЬ","минут"),("ДОСТИЖЕНИЯ","записей")]):
    c=tk.Frame(statrow,bg=PANEL,highlightthickness=1,highlightbackground=BORDER)
    c.pack(side="left",fill="both",expand=True,padx=(0,12 if i<2 else 0))
    text(c,heading,9,MUTED,True,bg=PANEL).pack(anchor="w",padx=18,pady=(16,4))
    v=text(c,"0",28,GREEN,True,bg=PANEL)
    v.pack(anchor="w",padx=18)
    text(c,unit,9,MUTED,bg=PANEL).pack(anchor="w",padx=18,pady=(0,15))
    stat_labels.append(v)
recent=panel(h)
text(recent,"ПОСЛЕДНИЕ ТРЕНИРОВКИ",12,WHITE,True,bg=PANEL).pack(anchor="w",pady=(0,10))
recent_label=text(recent,"Пока нет записей",11,MUTED,bg=PANEL,justify="left")
recent_label.pack(anchor="w")

# Workouts
w=pages["work"]
form=panel(w)
text(form,"НОВАЯ ТРЕНИРОВКА",12,GREEN,True,bg=PANEL).pack(anchor="w")
activity=entry(form,"Активность (например, дзюдо, плавание, ходьба)")
minutes=entry(form,"Продолжительность в минутах")
note=entry(form,"Заметка (необязательно)")
def add_work():
    try:
        mins=int(minutes.get())
        if not 1<=mins<=1440:raise ValueError
    except ValueError:
        messagebox.showerror("Проверь данные","Укажи продолжительность от 1 до 1440 минут.")
        return
    if not activity.get().strip():
        messagebox.showerror("Проверь данные","Напиши название активности.")
        return
    db.execute("INSERT INTO workouts(day,activity,minutes,note) VALUES(?,?,?,?)",
               (date.today().isoformat(),activity.get().strip(),mins,note.get().strip()))
    db.commit()
    for e in (activity,minutes,note):e.delete(0,"end")
    refresh()
button(form,"+  Сохранить тренировку",add_work).pack(anchor="w",pady=(15,0))
wl=panel(w)
text(wl,"ИСТОРИЯ ТРЕНИРОВОК",12,WHITE,True,bg=PANEL).pack(anchor="w")
wt=table(wl,("Дата","Активность","Минуты","Заметка"))

# Food
f=pages["food"]
ff=panel(f)
text(ff,"НОВАЯ ЗАПИСЬ",12,GREEN,True,bg=PANEL).pack(anchor="w")
meal=entry(ff,"Приём пищи (например, завтрак)")
description=entry(ff,"Что было на тарелке?")
def add_food():
    if not meal.get().strip() or not description.get().strip():
        messagebox.showerror("Проверь данные","Заполни оба поля.")
        return
    db.execute("INSERT INTO meals(day,meal,description) VALUES(?,?,?)",
               (date.today().isoformat(),meal.get().strip(),description.get().strip()))
    db.commit()
    meal.delete(0,"end");description.delete(0,"end")
    refresh()
button(ff,"+  Сохранить запись",add_food).pack(anchor="w",pady=(15,0))
fl=panel(f)
text(fl,"ДНЕВНИК ПИТАНИЯ",12,WHITE,True,bg=PANEL).pack(anchor="w")
ft=table(fl,("Дата","Приём пищи","Описание"))

# Progress chart (native canvas, no dependencies)
p=pages["progress"]
pc=panel(p)
text(pc,"АКТИВНОСТЬ ЗА ПОСЛЕДНИЕ 7 ДНЕЙ",12,GREEN,True,bg=PANEL).pack(anchor="w")
chart=tk.Canvas(pc,height=240,bg=PANEL,highlightthickness=0)
chart.pack(fill="x",pady=(16,8))
pl=panel(p)
progress_info=text(pl,"",12,WHITE,bg=PANEL,justify="left")
progress_info.pack(anchor="w")

# Achievements
a=pages["achieve"]
af=panel(a)
text(af,"МОЯ НОВАЯ ПОБЕДА",12,GREEN,True,bg=PANEL).pack(anchor="w")
achievement=entry(af,"Например, освоил новый приём")
def add_achievement():
    val=achievement.get().strip()
    if not val:return
    db.execute("INSERT INTO goals(day,achievement) VALUES(?,?)",(date.today().isoformat(),val))
    db.commit();achievement.delete(0,"end");refresh()
button(af,"★  Добавить достижение",add_achievement).pack(anchor="w",pady=(15,0))
al=panel(a)
text(al,"МОИ ДОСТИЖЕНИЯ",12,WHITE,True,bg=PANEL).pack(anchor="w")
at=table(al,("Дата","Достижение"))

# Helper
c=pages["coach"]
cf=panel(c,padx=26,pady=25)
text(cf,"✦  ТВОЙ ПОМОЩНИК",13,GREEN,True,bg=PANEL).pack(anchor="w")
text(cf,"Выбери тему",20,WHITE,True,bg=PANEL).pack(anchor="w",pady=(8,16))
advice=text(cf,"Выбери карточку ниже, чтобы увидеть рекомендацию.",12,MUTED,
            bg=PANEL,justify="left",wraplength=650)
advice.pack(anchor="w",pady=(0,22))
tips=[
    ("⚡  Перед тренировкой","Начни с разминки и постепенно увеличивай нагрузку. Ориентируйся на самочувствие."),
    ("◉  Восстановление","Отдых и полноценный сон помогают восстанавливаться. При боли или сильном утомлении снизь нагрузку."),
    ("▣  Регулярность","Выбирай реалистичный режим тренировок. Даже короткая умеренная активность может быть полезной."),
    ("◈  Питание","Старайся питаться разнообразно и регулярно. Для тренировок важно получать достаточно энергии и воды."),
]
for heading,msg in tips:
    button(cf,heading,lambda m=msg:advice.config(text=m),False).pack(anchor="w",pady=5)
text(cf,"Помощник работает по заранее подготовленным советам, без подключения к ИИ.",
     9,MUTED,bg=PANEL).pack(anchor="w",pady=(20,0))

def draw_chart():
    chart.delete("all")
    width=max(chart.winfo_width(),500)
    height=240
    values=[]
    days=[]
    for offset in range(6,-1,-1):
        d=date.today()-timedelta(days=offset)
        v=db.execute("SELECT COALESCE(SUM(minutes),0) FROM workouts WHERE day=?",
                     (d.isoformat(),)).fetchone()[0]
        values.append(v);days.append(d.strftime("%d.%m"))
    peak=max(max(values),30)
    left=35;right=width-20;bottom=205;top=20
    chart.create_line(left,bottom,right,bottom,fill=BORDER,width=2)
    step=(right-left)/7
    for i,(val,day) in enumerate(zip(values,days)):
        x=left+step*(i+0.5)
        bh=(val/peak)*(bottom-top)
        chart.create_rectangle(x-18,bottom-bh,x+18,bottom,
                               fill=GREEN if val else PANEL2,outline="")
        chart.create_text(x,bottom+18,text=day,fill=MUTED,font=(FONT,9))
        if val:chart.create_text(x,bottom-bh-12,text=str(val),fill=WHITE,font=(FONT,9,"bold"))
def refresh():
    count,total=db.execute("SELECT COUNT(*),COALESCE(SUM(minutes),0) FROM workouts").fetchone()
    achievements=db.execute("SELECT COUNT(*) FROM goals").fetchone()[0]
    for label,val in zip(stat_labels,(count,total,achievements)):label.config(text=str(val))
    rows=db.execute("SELECT day,activity,minutes FROM workouts ORDER BY id DESC LIMIT 4").fetchall()
    recent_label.config(text="\n".join(f"●  {day}    {name}  ·  {mins} мин" for day,name,mins in rows)
                        if rows else "Добавь первую тренировку, и она появится здесь.")
    update_table(wt,"SELECT day,activity,minutes,note FROM workouts ORDER BY id DESC LIMIT 100")
    update_table(ft,"SELECT day,meal,description FROM meals ORDER BY id DESC LIMIT 100")
    update_table(at,"SELECT day,achievement FROM goals ORDER BY id DESC LIMIT 100")
    thisweek=db.execute("SELECT COALESCE(SUM(minutes),0) FROM workouts WHERE day>=?",
                        ((date.today()-timedelta(days=6)).isoformat(),)).fetchone()[0]
    progress_info.config(text=f"Всего тренировок: {count}     •     За последние 7 дней: {thisweek} минут активности")
    root.after_idle(draw_chart)
chart.bind("<Configure>",lambda event:draw_chart())
show("home")
root.mainloop()
