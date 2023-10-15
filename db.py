import psycopg2
import os
import face_recognition
import numpy
from dotenv import load_dotenv
from verifica_clareza import detectar_rosto_na_imagem

load_dotenv()

class BancoDeDados:

    @staticmethod
    def conexao(self):
        try:
            connection = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
        except Exception as e:
            print(e)
        return connection

    def execute(self,SQL):
        connection = self.conexao(self)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SQL)

    def querry(self,SQL):
        connection = self.conexao(self)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SQL)
                results = cursor.fetchall()
        return results

    def get_workers(self):
        SQL = "SELECT * FROM workers"
        response = self.querry(SQL)
        return response

    def check_worker_encryption(self):
        workers = self.get_workers()
        for worker in workers:
            if worker[3] is None:
                coded_str = self.encode_image_str(worker[2])
                self.execute(f"UPDATE workers SET image_coded = '{coded_str}' WHERE id = {worker[0]}")
                print(f"funcionario {worker[1]} atualizado com a versão encoded de sua imagem")
            else:
                print(f"Imagem do funcionario {worker[1]} ja esta encoded")


    def check_if_worker(self,image):
        workers = self.get_workers()
        imagem_a_comparar = face_recognition.load_image_file(image)
        imagem_a_comparar = face_recognition.face_encodings(imagem_a_comparar)
        for worker in workers:
            print(worker)
            encoded_image = self.str_to_encoded(worker[3])
            print(face_recognition.compare_faces(encoded_image,imagem_a_comparar)[0])
            if face_recognition.compare_faces(encoded_image,imagem_a_comparar)[0]:
                return f"Funcionario {worker[1]} indentificado"

        return f"Funcionario nao indentificado"


    def encode_image_str(self,image):
        imagem = face_recognition.load_image_file(image)
        codificacao = face_recognition.face_encodings(imagem)[0]
        codificacao = str(codificacao)
        codificacao = codificacao.replace("[","").replace("]","").replace("\n", "")
        return codificacao

    def str_to_encoded(self,array_in_str):
        codificacao = numpy.fromstring(array_in_str, sep=" ")
        return codificacao


DB = BancoDeDados()
path = "images/du_sem_oculos.PNG"
DB.check_worker_encryption()
if detectar_rosto_na_imagem(path):
    print(DB.check_if_worker(path))
else:
    print("clareza insatisfatorio")
