from flask import Flask, render_template, request

import oracledb

import json

with open("senha.json") as f:
    credenciais = json.load(f)

USER = credenciais["user"]
PASS = credenciais["pass"]

HOST = "oracle.fiap.com.br"
PORT = 1521
SID = "ORCL"

dsnStr = oracledb.makedsn("oracle.fiap.com.br", 1521, "ORCL")

connection = oracledb.connect(user=USER, password=PASS, dsn=dsnStr)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('menu.html')


@app.route('/inserir_cliente', methods=['POST', 'GET'])
def inserir_cliente():
    if request.method == 'POST':
        try:
            cursor = connection.cursor()
            nome = request.form.get('nome')
            email = request.form.get('email')
            cpf = int(request.form.get('cpf'))
            telefone = int(request.form.get('telefone'))
            tipo_deficiencia = request.form.get('tipo_deficiencia')
            sql = "INSERT INTO cliente (nm_cliente, email, nr_cpf, nr_telefone, tipo_deficiencia) VALUES (:1, :2, :3, :4, :5)"
            cursor.execute(sql, [nome, email, cpf, telefone, tipo_deficiencia])
            connection.commit()
            return "Cliente Inserido"
        except oracledb.DatabaseError as e:
            error, = e.args
            return f"Ocorreu um erro: {error.code} - {error.message}"
        finally:
            cursor.close()

    else:
        return render_template('inserir.html')



@app.route('/visu_clientes')
def visu_clientes():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM cliente")
        rows = cursor.fetchall()
        clientes = []
        for row in rows:
            cliente = {
                'nome': row[0],
                'email': row[1],
                'cpf': row[2],
                'telefone': row[3],
                'tipo_deficiencia': row[4]
            }
            clientes.append(cliente)
        return render_template('visu_clientes.html', clientes=clientes)
    except oracledb.DatabaseError as e:
        error, = e.args
        return f"Ocorreu um erro:: {error.code} - {error.message}"


@app.route('/att_cliente', methods=['POST', 'GET'])
def att_cliente():
    if request.method == 'POST':
        try:
            cpf = int(request.form.get('cpf'))
            novo_nome = request.form.get('nome')
            novo_email = request.form.get('email')
            novo_telefone = int(request.form.get('telefone'))
            novo_tipo_deficiencia = request.form.get('tipo_deficiencia')
            sql = "UPDATE cliente SET nm_cliente = :1, email = :2, nr_telefone = :3, tipo_deficiencia = :4 WHERE nr_cpf = :5"
            cursor = connection.cursor()
            cursor.execute(sql, [novo_nome, novo_email, novo_telefone, novo_tipo_deficiencia, cpf])
            connection.commit()
            return "Informações do cliente atualizadas com sucesso."
        except oracledb.DatabaseError as e:
            error, = e.args
            return f"Ocorreu um erro: {error.code} - {error.message}"
        finally:
            cursor.close()
    else:
        return render_template('att_cliente.html')


@app.route('/del_cliente', methods=['GET', 'POST'])
def del_cliente():
    if request.method == 'POST':
        cpf = request.form['cpf']
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM cliente WHERE nr_cpf = :1", [cpf])
            connection.commit()
            return "Cliente deletado"
        except oracledb.DatabaseError as e:
            error, = e.args
            return f"Ocorreu um erro:: {error.code} - {error.message}"
        finally:
            cursor.close()
    else:
        return render_template('del_cliente.html')

if __name__ == '__main__':
    app.run(debug=True)


