#Cadastro clientes
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import pandas as pd
import re
import os
conec=sqlite3.connect('Dados_Clientes.db')

cursor=conec.cursor()

# cursor.execute("""CREATE TABLE dados(
#         nome text NOT NULL,
#         gmail text NOT NULL,
#         cpf integer NOT NULL
#                             )
# """)
# conec.commit()
# conec.close()







#TELA
tela=Tk()
tela.title("Clientes Dados")
tela.geometry("300x300")
tela.minsize(300,300)
tela.maxsize(300,300)

#CODIGO COM BANCO
def adicionar():
    def cadastro_clientes():
        
        conec=sqlite3.connect('Dados_Clientes.db')
        curso=conec.cursor()
        
        curso.execute("INSERT INTO dados VALUES(:nome, :gmail, :cpf)",
                    {
                    'nome':entry_nome.get(),
                    'gmail':entry_gamil.get(),
                    'cpf':entry_cpf.get()
                    }
                    )

        
        pegacpg=(entry_cpf.get())
        pegag=(entry_gamil.get())
        pegan=(entry_nome.get())
        padrao= r'([a-zA-Z0-9_.-]+)@([a-zA-Z]+)([\.])([a-zA-Z]+)'


        if (pegan.isdigit()):
            messagebox.showerror("NOME INVALIDO","USE APENAS LETRAS!!!")
            entry_nome.delete(0,END)
            conec.close()
            return True
        
        elif pegan=='':
            messagebox.showwarning("NOME INVALIDO","ESTE CAMPO NÃO PODE ESTAR VAZIO!!!")
            conec.close()
            return True

        #verificação do email
        if pegag=='':
            messagebox.showwarning("EMAIL INVALIDO","ESTE CAMPO NÃO PODE ESTAR VAZIO!!!")
            conec.close()
            return True
        
        if  re.search(padrao,pegag)==None:
            messagebox.showwarning("EMAIL INVALIDO","DIGITE UM EMAIL VALIDO!!!")
            entry_gamil.delete(0,END)
            conec.close()
            return True

            
        #verificação do cpf, se contem 11 numeros ou nao   
        if pegacpg=='':
            messagebox.showwarning("CPF INVALIDO","ESTE CAMPO NÃO PODE ESTAR VAZIO!!!")
            conec.close()
            return True

        elif len(pegacpg)>11:
            messagebox.showerror("INVALIDO","O CPF DEVE CONTER 11 NÚMEROS!!!")
            entry_cpf.delete(0,END)
            conec.close()
            return True
        
        #validação cpf, se  contem numeros
        if  not (pegacpg.isdigit()):
            messagebox.showwarning("INVALIDO","CPF APENAS ACEITA NÚMEROS!!!")
            entry_cpf.delete(0,END)
            conec.close()
            return False
        else:
            messagebox.showinfo("VALIDO","Cadastro Realizado!")
            entry_nome.delete(0,END)
            entry_gamil.delete(0,END)
            entry_cpf.delete(0,END)
            conec.commit()
            conec.close()
            
    #CODIGO EXPORTAR PARA O EXCEL
    def exportar_excel():
        conec=sqlite3.connect('Dados_Clientes.db')

        cursor=conec.cursor()

        cursor.execute("SELECT *, oid FROM dados")
        motrcasdastro=cursor.fetchall()
        motrcasdastro=pd.DataFrame(motrcasdastro,columns=['nome','gmail','cpf','Id_Banco'])
        motrcasdastro.to_excel("Dados_dos_clientes.xlsx")
        conec.commit()
        conec.close()
        messagebox.showinfo("Exportado","Exportado com Sucesso!")

    #LABEL
    global label_nome
    label_nome=Label(tela,text='Nome', fg="Black",font=16)
    label_nome.grid(row=0,column=0,pady=(20,0))
    global label_gmail
    label_gmail= Label(tela,text='Gmail', fg='Black',font=16)
    label_gmail.grid(row=1,column=0,pady=(30,0))
    global label_cpf
    label_cpf= Label(tela,text='CPF', fg='Black',font=16)
    label_cpf.grid(row=2,column=0,pady=(40,0))

    #ENTRY
    global entry_nome
    entry_nome= Entry(tela,width=30,justify=CENTER,borderwidth=2,relief=SOLID)
    entry_nome.grid(row=0,column=1,padx=(20,0),pady=(20,0))

    global entry_gamil
    entry_gamil= Entry(tela,width=30,justify=CENTER,borderwidth=2,relief=SOLID)
    entry_gamil.grid(row=1,column=1,padx=(20,0),pady=(30,0))

    global entry_cpf
    entry_cpf= Entry(tela,width=30,justify=CENTER,borderwidth=2,relief=SOLID)
    entry_cpf.grid(row=2,column=1,padx=(20,0),pady=(40,0))

    #BOTAO
    global botao_cadastro
    botao_cadastro= Button(tela,text='Cadastrar Cliente',font=12,relief=SOLID,command=cadastro_clientes)
    botao_cadastro.grid(row=3,column=1,pady=(20,0),padx=(15,0))

    global botao_excel
    botao_excel= Button(tela,text='Exportar para o Excel',font=12,relief=SOLID,command=exportar_excel)
    botao_excel.grid(row=4,column=1,pady=(20,0),padx=(15,0),ipadx=20)
    



        

def Verdados():
    tela2=Toplevel()
    tela2.geometry('500x350')
    tela2.maxsize(500,350)
    tela2.title('Acesso aos Registros')

    global tv
    tv=ttk.Treeview(tela2,columns=('Nome','Email','CPF','ID'),show='headings')
    tv.column('Nome',minwidth=0,width=100,)
    tv.column('Email',minwidth=0,width=150)
    tv.column('CPF',minwidth=0,width=100)
    tv.column('ID',minwidth=0,width=50)

    tv.heading('Nome',text='Nome')
    tv.heading('Email',text='Email')
    tv.heading('CPF',text='CPF')
    tv.heading('ID',text='ID')
    tv.grid(padx=(50,0),pady=(10,0))

    conec=sqlite3.connect('Dados_Clientes.db')

    cursor=conec.cursor()
    
    cursor.execute("SELECT *, oid FROM dados")
    motrcasdastro=cursor.fetchall()
    for i in motrcasdastro:
        tv.insert("",'end',values=i)
    
    global nome_atualizado
    nome_atualizado=Entry(tela2,relief=SUNKEN,borderwidth=2,justify=CENTER,font=("Arial",10),width=24)
    nome_atualizado.grid(row=1,column=0,pady=(10,0),padx=(0,150))

    global gmail_atualizado
    gmail_atualizado=Entry(tela2,relief=SUNKEN,borderwidth=2,justify=CENTER,font=("Arial",10),width=24)
    gmail_atualizado.grid(row=1,column=0,pady=(10,0),padx=(280,0))

    global CPF_atualizado
    CPF_atualizado=Entry(tela2,relief=SUNKEN,borderwidth=2,justify=CENTER,font=("Arial",10),width=17)
    CPF_atualizado.grid(row=2,column=0,padx=(60,0),pady=(4,0))


    dele=Button(tela2,text='Deletar',font=('Arial',11),relief=SOLID,bg='#ffa654',command=deletar)
    dele.grid(row=3,column=0,pady=(10,0),padx=(0,60))
    
    atual=Button(tela2,text='Atualizar',font=('Arial',11),relief=SOLID,bg='#6cb6e3',command=atualizar)
    atual.grid(row=3,column=0,pady=(10,0),padx=(140,0))

    tv.bind("<ButtonRelease-1>",selecionar)




#FUNÇÃO ATUALIZAR
def selecionar(e):
    nome_atualizado.delete(0,END)
    gmail_atualizado.delete(0,END)
    CPF_atualizado.delete(0,END)

    pegar=tv.focus()
    valores=tv.item(pegar,'values')

    nome_atualizado.insert(0,valores[0])
    gmail_atualizado.insert(0,valores[1])
    CPF_atualizado.insert(0,valores[2])

def atualizar():
    pegar= tv.selection()
    for i in pegar:
        id_num= tv.item(i,'values')[3]
    pegar1=tv.focus()
    valores=tv.item(pegar1,text='',values=(nome_atualizado.get(),gmail_atualizado.get(),CPF_atualizado.get(),id_num,))
    


    conec=sqlite3.connect('Dados_Clientes.db')
    curso=conec.cursor()

    curso.execute("""UPDATE dados SET
        nome= :nome1,
        gmail= :gmail1,
        cpf= :cpf1
                    
        WHERE oid= :oid""",
        {
            'nome1':nome_atualizado.get(),
            'gmail1':gmail_atualizado.get(),
            'cpf1':CPF_atualizado.get(),
            'oid': id_num
        })
    conec.commit()
    conec.close()

    nome_atualizado.delete(0,END)
    gmail_atualizado.delete(0,END)
    CPF_atualizado.delete(0,END)

 #FUNÇÃO DE DELETAR   
def deletar():
    pegar= tv.selection()
    for i in pegar:
        id_num= tv.item(i,'values')[3]
        tv.delete(i)
    messagebox.showinfo("Cadastro deletado","Cadastro deletado com sucesso!")
    conec=sqlite3.connect('Dados_Clientes.db')
    curso=conec.cursor()
    curso.execute("DELETE FROM dados WHERE oid= ?", (id_num,))
    conec.commit()
    conec.close()
    nome_atualizado.delete(0,END)
    gmail_atualizado.delete(0,END)
    CPF_atualizado.delete(0,END)
    
    

#CRIANDO BARRA DE MENU

barraM=Menu(tela)
menuB=Menu(barraM,tearoff=0)
barraM.add_cascade(label="Banco",menu=menuB)
menuB.add_command(label="Adicionar",command=adicionar)
menuB.add_separator()
menuB.add_command(label='Ver dados',command=Verdados)



tela.config(menu=barraM)



tela.mainloop()