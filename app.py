#MySQL 관련 코드 - 정기용
# 필요한 라이브러리 import
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file
import ctypes
import os
import zipfile
import time
from werkzeug.utils import secure_filename
import csv
from datetime import datetime
import pymysql

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'slo12131422.',
    'database': 'hobbyhive',
    'charset': 'utf8mb4'
}

app = Flask(__name__)
app.secret_key = 'dkssud!dlrjs!vmfaldxlavmfzhemdla~' # 세션 암호화 위한 키

user_csv_file_path = os.path.join(os.path.dirname(__file__), r'static\user.csv')  # CSV 파일 경로
classes_csv_file_path = os.path.join(os.path.dirname(__file__), r'static\classes.csv')
applications_csv_file_path = os.path.join(os.path.dirname(__file__), r'static\applications.csv')
comments_csv_file_path = os.path.join(os.path.dirname(__file__), r'static\comments.csv')
community_posts_csv_file_path = os.path.join(os.path.dirname(__file__), r'static\community_posts.csv')
likes_csv_file_path = os.path.join(os.path.dirname(__file__), r'static\likes.csv')

UPLOAD_FOLDER = 'static/uploads' # 회원가입에서 업로드한 파일 관리
USER_INFO_FOLDER = 'static/users' # admin에게 전달할 사용자 정보 폴더
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['USER_INFO_FOLDER'] = USER_INFO_FOLDER

# 폴더들이 없다면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(USER_INFO_FOLDER):
    os.makedirs(USER_INFO_FOLDER)

# C에서 구현한 함수를 사용하기 위해 dll파일 불러옴
c_function = ctypes.CDLL(os.path.join(os.path.dirname(__file__), r'c_function\C_function.dll'))

# 로그인 함수
c_function.login.restype = ctypes.c_int
c_function.login.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

# 회원가입 요청 함수
c_function.signup_request.restype = ctypes.c_bool
c_function.signup_request.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

# 아이디 중복확인 함수
c_function.duplicate_check.restype = ctypes.c_bool
c_function.duplicate_check.argtypes = [ctypes.c_char_p]

# 회원가입 수락 함수
c_function.signup_accept.restype = ctypes.c_bool
c_function.signup_accept.argtypes = [ctypes.c_char_p]

# 회원가입 거절 함수
c_function.signup_reject.restype = ctypes.c_bool
c_function.signup_reject.argtypes = [ctypes.c_char_p]

# delete_user 함수 설정
c_function.delete_user.restype = ctypes.c_bool
c_function.delete_user.argtypes = [ctypes.c_char_p]

# is_user_mentor 함수 정의
c_function.is_user_mentor.argtypes = [ctypes.c_char_p]
c_function.is_user_mentor.restype = ctypes.c_bool

# save_class_info 함수 정의
c_function.save_class_info.argtypes = [ctypes.c_char_p] * 8
c_function.save_class_info.restype = ctypes.c_bool

# apply_class_in_c 함수 정의
c_function.apply_class_in_c.argtypes = [ctypes.c_char_p]
c_function.apply_class_in_c.restype = ctypes.c_bool

# change_id 함수 설정
c_function.change_id.restype = ctypes.c_bool
c_function.change_id.argtypes = [ctypes.c_char_p]

# change_password 함수 설정
c_function.change_password.restype = ctypes.c_bool
c_function.change_password.argtypes = [ctypes.c_char_p]

# save_community_post 함수 정의
c_function.save_community_post.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
c_function.save_community_post.restype = None

# 함수 설정 (is_user_valid는 int를 반환하고, char * 타입의 인자를 받음)
c_function.is_user_valid.restype = ctypes.c_int
c_function.is_user_valid.argtypes = [ctypes.c_char_p]

c_function.is_liked_by_user.restype = ctypes.c_bool  # 반환값은 bool
c_function.is_liked_by_user.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  # 두 개의 char* 인자를 받음

c_function.delete_comment.restype = ctypes.c_bool
c_function.delete_comment.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

# -----------------------------정인성 ----------------------------
# admin페이지에서 보여줄 내용 (회원가입 대기자) 저장하는 리스트
signup_data = []

def export_mysql_to_csv(csv_file_path, table_name):
    try:
        # MySQL 데이터베이스 연결
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # 데이터 조회 쿼리
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            rows = cursor.fetchall()

            # CSV 파일로 데이터 쓰기 (헤더 제외)
            with open(csv_file_path, 'w', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)  # 데이터만 작성
                
    except FileNotFoundError:
        print(f"지정된 경로에 파일을 생성할 수 없습니다: {csv_file_path}")
    except pymysql.MySQLError as e:
        print(f"MySQL 오류: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()

table_name_users = 'users'  # MySQL 테이블 이름
table_name_classes = 'classes'
table_name_applications = 'applications'
table_name_comments = 'comments'
table_name_community_posts = 'community_posts'
table_name_likes = 'likes'


def export_sql_csv() :
    export_mysql_to_csv(user_csv_file_path, table_name_users)
    export_mysql_to_csv(classes_csv_file_path,table_name_classes)
    export_mysql_to_csv(applications_csv_file_path,table_name_applications)
    export_mysql_to_csv(comments_csv_file_path,table_name_comments)
    export_mysql_to_csv(community_posts_csv_file_path,table_name_community_posts)
    export_mysql_to_csv(likes_csv_file_path,table_name_likes)

export_sql_csv()

# 로그인 페이지 -> 실행되면 login.html 실행
@app.route('/')
def login_page():
    return render_template('login.html')

# 로그인 시도 받으면 처리하는 라우트
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = data['id'].encode('utf-8')
    user_password = data['password'].encode('utf-8')
    
    # 기존 CSV 기반 로그인 처리
    login_rst = c_function.login(user_id, user_password)

    # MySQL 데이터와 비교
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            query = "SELECT status, role FROM users WHERE id=%s AND pw=%s"
            cursor.execute(query, (user_id.decode('utf-8'), user_password.decode('utf-8')))
            mysql_result = cursor.fetchone()

            if mysql_result:
                mysql_status, mysql_role = mysql_result
                if mysql_status == 'approved' and login_rst == 2:
                    session['admin'] = True
                    return jsonify({"success": True, "redirect": "/admin"})
                elif mysql_status == 'approved' and login_rst == 1:
                    session['user_id'] = user_id
                    session['user_password'] = user_password # 세션에 비밀번호 저장
                    return jsonify({"success": True, "redirect": "/main"})
                elif mysql_status == 'pending':
                    return jsonify({"success": False, "message": "관리자 승인 대기중입니다."})
                elif mysql_status == 'rejected':
                    session['rejected_user'] = data['id']
                    return jsonify({"success": False, "message": "회원가입이 거절되었습니다."})
    except pymysql.MySQLError as e:
        print(f"MySQL 오류: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()

    # 기본 실패 응답
    return jsonify({"success": False, "message": "아이디 또는 비밀번호가 잘못되었습니다."})

# 회원가입 처리하는 라우트
@app.route('/sign_up.html', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        return render_template('sign_up.html')
    
    try:
        # 사용자 정보 저장
        user_id = request.form['id']
        user_password = request.form['password']
        user_status = 'pending'  # 회원가입 진행 상태 나타내는 정보
        user_role = request.form['role']  # mento 또는 mentee
        user_name = request.form['name']
        user_birthday = request.form['birthday']
        user_gender = request.form['gender']

        # 경로 설정
        user_info_folder = os.path.join(USER_INFO_FOLDER, f"{user_id}_info.txt")

        uploaded_files = [] # 업로드된 파일 모으는 리스트
        for file in request.files.getlist('files'):
            original_filename = secure_filename(file.filename)  # 원본 파일 이름
            extension = os.path.splitext(original_filename)[1]  # 파일 확장자 추출
            new_filename = f"{user_id}{extension}"  # 새로운 파일 이름
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(file_path)
            uploaded_files.append(file_path)

        # 기존 코드(C DLL 호출) 유지
        result = c_function.signup_request(
            user_id.encode('utf-8'), 
            user_password.encode('utf-8'), 
            user_status.encode('utf-8'),
            user_role.encode('utf-8'),
            user_name.encode('utf-8'), 
            user_birthday.encode('utf-8'),
            user_gender.encode('utf-8')
        )
        
         # 사용자가 업로드한 파일을 압축 => admin페이지에서 다운받아서 확인 가능
        zip_filename = f"{user_id}_files.zip"
        zip_path = os.path.join(USER_INFO_FOLDER, zip_filename)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            txt_file_path = os.path.join(USER_INFO_FOLDER, f"{user_id}_info.txt")
            zipf.write(txt_file_path, os.path.basename(txt_file_path))
            for file_path in uploaded_files:
                zipf.write(file_path, os.path.basename(file_path))

        signup_data.append({
            'id': user_id,
            'apply_date': time.strftime("%Y.%m.%d"),
            'role': user_role,
            'zip_path': zip_path
        })

        # MySQL에 회원가입 데이터 저장
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                # 중복 ID 확인
                check_query = "SELECT id FROM users WHERE id = %s"
                cursor.execute(check_query, (user_id,))
                existing_user = cursor.fetchone()
                if existing_user:
                    return jsonify({"success": False, "message": "ID가 이미 존재합니다."})

                # 데이터 삽입
                insert_query = """
                INSERT INTO users (id, pw, status, role, name, birthday, gender)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (user_id, user_password, user_status, user_role, user_name, user_birthday, user_gender))
                connection.commit()
        except pymysql.MySQLError as e:
            print(f"MySQL 오류: {e}")
            return jsonify({"success": False, "message": "데이터베이스 오류"})
        finally:
            if 'connection' in locals() and connection:
                connection.close()

        # 사용자 정보 파일 생성
        try:
            with open(user_info_folder, 'w', encoding='utf-8') as f:
                f.write(f"ID: {user_id}\nPassword: {user_password}\nStatus: {user_status}\n"
                        f"Role: {user_role}\nName: {user_name}\nBirthday: {user_birthday}\nGender: {user_gender}\n")
        except FileNotFoundError as e:
            print(f"파일 생성 오류: {e}")
            return jsonify({"success": False, "message": "파일 생성 오류"})

        # 성공 응답
        return jsonify({"success": True, "message": "회원가입 요청이 성공적으로 처리되었습니다."})
    except Exception as e:
        print(f"오류 발생: {e}")
        return jsonify({"success": False, "message": f"서버 오류: {str(e)}"})



# 회원가입 수락하는 라우트
@app.route('/signup_accept/<user_id>', methods=['POST'])
def accept_signup(user_id):

    result = c_function.signup_accept(user_id.encode('utf-8'))
    
    if result:
        global signup_data
        # 회원가입 대기자 명단에서 회원가입 수락된 사람 제거
        signup_data = [x for x in signup_data if x['id'] != user_id]

        # MySQL에서 status 업데이트
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                update_query = "UPDATE users SET status = %s WHERE id = %s"
                cursor.execute(update_query, ('approved', user_id))
                connection.commit()
        except pymysql.MySQLError as e:
            print(f"MySQL 오류: {e}")
        finally:
            if 'connection' in locals() and connection:
                connection.close()

        return jsonify({"success": True})
    
    return jsonify({"success": False})

# 회원가입 거절하는 라우트
@app.route('/signup_reject/<user_id>', methods=['POST'])
def reject_signup(user_id):
    # 기존 코드 실행
    result = c_function.signup_reject(user_id.encode('utf-8'))
    
    if result:
        global signup_data
        # 회원가입 대기자 명단에서 회원가입 거절된 사람 제거
        signup_data = [signup for signup in signup_data if signup['id'] != user_id]

        # MySQL에서 status 업데이트
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                update_query = "UPDATE users SET status = %s WHERE id = %s"
                cursor.execute(update_query, ('rejected', user_id))
                connection.commit()
        except pymysql.MySQLError as e:
            print(f"MySQL 오류: {e}")
        finally:
            if 'connection' in locals() and connection:
                connection.close()

        return jsonify({"success": True})
    
    return jsonify({"success": False})


@app.route('/delete_rejected_user', methods=['POST'])
def confirm_rejection():
    # 세션에서 거절된 사용자 ID를 가져옴
    user_id = session.pop('rejected_user', None)
    
    if user_id:
        # delete_user 함수로 사용자의 모든 정보 삭제
        result = c_function.delete_user(user_id.encode('utf-8'))  # 해당 ID에 대한 정보 삭제
        
        if result:
            # MySQL에서 해당 사용자 정보 삭제
            try:
                connection = pymysql.connect(**db_config)
                with connection.cursor() as cursor:
                    delete_query = "DELETE FROM users WHERE id = %s"
                    cursor.execute(delete_query, (user_id,))
                    connection.commit()
                    print(f"MySQL에서 사용자 '{user_id}'의 정보를 삭제했습니다.")
            except pymysql.MySQLError as e:
                print(f"MySQL 오류: {e}")
            finally:
                if 'connection' in locals() and connection:
                    connection.close()
            
            return jsonify({"success": True})
    
    return jsonify({"success": False})

# 아이디 중복 확인 라우트
@app.route('/check_duplicate', methods=['POST'])
def check_duplicate():
    user_id = request.json['id'].encode('utf-8')
    is_duplicate = c_function.duplicate_check(user_id)
    return jsonify({"is_duplicate": is_duplicate})

# admin페이지에서 사용자 정보, 제출 서류를 모은 zip파일 다운받는 라우트
@app.route('/download_zip/<user_id>')
def download_zip(user_id):
    user_zip_path = None
    for x in signup_data:
        if x['id'] == user_id:
            user_zip_path = x['zip_path']
            break  # 첫 번째로 조건을 만족하는 항목을 찾으면 루프 종료

    if user_zip_path and os.path.exists(user_zip_path):
        return send_file(user_zip_path, as_attachment=True, download_name=f"{user_id}_files.zip", mimetype='application/zip')
    return "파일을 찾을 수 없습니다.", 404

# admin페이지 라우트
@app.route('/admin')
def admin_page():
    signup_data.clear()  # 기존 데이터를 초기화
    
    # CSV 파일에서 대기열 사용자 데이터 읽기
    try:
        with open('static/user.csv', 'r', encoding='UTF-8') as file:
            for line in file:
                user_info = line.strip().split(',')
                if len(user_info) < 7:
                    continue
                
                id, pw, status, role, name, birthday, gender = user_info
                
                # 'pending' 상태인 사용자만 대기열에 추가
                if status == 'pending':
                    signup_data.append({
                        'id': id,
                        'apply_date': time.strftime("%Y.%m.%d"), 
                        'role': role,
                        'zip_path': f'static/users/{id}_files.zip'  # 파일 경로 설정
                    })
    except FileNotFoundError:
        print("user.csv 파일을 찾을 수 없습니다.")

    return render_template('admin.html', signup_data=signup_data)

# admin페이지 로그아웃 라우트
@app.route('/admin_logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('login_page'))

@app.route('/user_logout')
def user_logout():
    session.pop('user_id', None)
    session.pop('user_password', None)
    return redirect(url_for('login_page'))

# ----------------------------- 임수빈 ----------------------------

def is_user_mentor(user_id):
    # user_id가 str 타입이면 encode()를 호출하여 bytes로 변환
    if isinstance(user_id, str):
        user_id = user_id.encode('utf-8')
    
    # 이후 C 함수 호출
    return c_function.is_user_mentor(user_id)


# save_class_info 함수 불러오기
def save_class_in_c(class_title, mentor_id, location, class_description, price, mode, capacity, image_path):
    class_title_bytes = class_title.encode('utf-8')
    mentor_id_bytes = mentor_id.encode('utf-8')
    location_bytes = location.encode('utf-8')
    class_description_bytes = class_description.encode('utf-8')
    price_bytes = price.encode('utf-8')
    mode_bytes = mode.encode('utf-8')
    capacity_bytes = capacity.encode('utf-8')
    image_path_bytes = image_path.encode('utf-8')
    return c_function.save_class_info(class_title_bytes, mentor_id_bytes, location_bytes, 
                               class_description_bytes, price_bytes, mode_bytes, capacity_bytes, image_path_bytes) # C 함수 호출

def load_classes_from_c():
    classes = []
    try:
        with open('static/classes.csv', 'r', encoding='utf-8') as csvfile:
            for line in csvfile:
                fields = line.strip().split(',')
                if len(fields) == 10:  # 필드 개수 확인
                    # 클래스 정보를 딕셔너리 형태로 추가
                    class_title, mentor_id, location, class_description, price, mode, capacity, current_applicants, image_path, tags = fields
                    classes.append({
                        'class_title': class_title,
                        'mentor_id': mentor_id,
                        'location': location,
                        'class_description': class_description,
                        'price': price,
                        'mode': mode,
                        'capacity': int(capacity),
                        'current_applicants': int(current_applicants),
                        'image_path': image_path,
                        'tags': tags
                    })
    except FileNotFoundError:
        pass  # 파일이 없을 경우 예외 처리

    return classes



# 메인 페이지
@app.route('/main')
def main():
    classes = load_classes_from_c()  # csv 파일에서 클래스 정보 불러오기
    role = session.get('role', 'mentee')  # 현재 로그인된 사용자의 역할 확인
    posts = load_community_posts()
    return render_template('main.html', classes=classes, user_role=role, posts=posts)

@app.route('/class_page')
def class_page():
    classes = load_classes_from_c()  # csv 파일에서 클래스 정보 불러오기
    role = session.get('role', 'mentee')  # 현재 로그인된 사용자의 역할 확인
    return render_template('class.html', classes=classes, user_role=role)

@app.route('/check_mentor')
def check_mentor():
    user_id = session.get('user_id')  # 세션에서 사용자 아이디를 가져옵니다.
    # 세션에 user_id가 없으면 로그인 페이지로 리다이렉트
    if not user_id:
        return redirect(url_for('login'))  # 'login'은 로그인 페이지를 처리하는 함수명입니다.
    
    # 멘토 여부 확인
    if is_user_mentor(user_id):
        print("pmentor")
        return {'status': 'mentor'}
    else:
        print("pmentee`")
        return {'status': 'mentee'}
    
# 클래스 생성 페이지로 이동
@app.route('/create_class', methods=['GET'])
def create_class_form():
    return render_template('create_class.html')

# 클래스 생성 요청 처리
@app.route('/create_class', methods=['POST'])
def create_class():
    try:
        # 클래스 정보 추출
        class_title = request.form['class_title']
        mentor_id = request.form['mentor_id']
        location = request.form['location']
        class_description = request.form['class_description']
        price = request.form['price']
        mode = request.form['mode']
        capacity = request.form['capacity']
        tags = request.form['tags']
        image = request.files['class_image']

        # 이미지 저장 경로 설정 & 저장
        image_filename = image.filename
        image_path = os.path.join('images/class_image', image_filename).replace("\\", "/")
        image.save(os.path.join('static', image_path))

        current_applicants = 0  # 신청 인원 초기값 0으로 설정

        # C DLL을 사용하여 클래스 정보 저장
        result = c_function.save_class_info(
            class_title.encode('utf-8'),
            mentor_id.encode('utf-8'),
            location.encode('utf-8'),
            class_description.encode('utf-8'),
            price.encode('utf-8'),
            mode.encode('utf-8'),
            capacity.encode('utf-8'),
            image_path.encode('utf-8'),
            tags.encode('utf-8')
        )

        # MySQL 데이터 저장
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                query = """
                INSERT INTO classes (
                    class_title, mentor_id, location, class_description,
                    price, mode, capacity, current_applicants, image_path, tags
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    class_title, mentor_id, location, class_description,
                    price, mode, capacity, current_applicants, image_path, tags
                ))
                connection.commit()
        except pymysql.MySQLError as e:
            print(f"MySQL 오류: {e}")
        finally:
            if 'connection' in locals() and connection:
                connection.close()

        return redirect(url_for('main'))
    except Exception as e:
        print(f"Error creating class: {e}")
        return jsonify({"success": False, "message": "Failed to create class"}), 500


# 특정 클래스의 세부 정보 표시
@app.route('/class_details/<class_title>', methods=['GET'])
def class_details(class_title):
    class_details = {}
    class_details_str = ctypes.create_string_buffer(1024)

    # C 함수 호출
    success = c_function.load_class_details(class_title.encode('utf-8'), class_details_str)
    if success:
        details = class_details_str.value.decode('utf-8').strip().split(',')
        if len(details) == 10:
            class_details = {
                'class_title': details[0],
                'mentor_id': details[1],
                'location': details[2],
                'class_description': details[3],
                'price': details[4],
                'mode': details[5],
                'capacity': int(details[6]),
                'current_applicants': int(details[7]) if details[7] is not None else 0,
                'image_path': details[8],
                'tags': details[9]
            }
    else:
        print("C 함수 호출 실패, MySQL에서 데이터 로드 시도.")

    # MySQL에서 클래스 정보를 가져오는 부분
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            query = """
            SELECT class_title, mentor_id, location, class_description, price, mode, capacity, 
                   current_applicants, image_path, tags
            FROM classes
            WHERE class_title = %s
            """
            cursor.execute(query, (class_title,))
            mysql_details = cursor.fetchone()

            if mysql_details:
                class_details = {
                    'class_title': mysql_details[0],
                    'mentor_id': mysql_details[1],
                    'location': mysql_details[2],
                    'class_description': mysql_details[3],
                    'price': mysql_details[4],
                    'mode': mysql_details[5],
                    'capacity': int(mysql_details[6]),
                    'current_applicants': int(mysql_details[7]) if mysql_details[7] is not None else 0,
                    'image_path': mysql_details[8],
                    'tags': mysql_details[9]
                }
            else:
                return "클래스를 찾을 수 없습니다.", 404
    except pymysql.MySQLError as e:
        print(f"MySQL 오류: {e}")
        return "서버 오류가 발생했습니다.", 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()

    return render_template('class_details.html', class_details=class_details)


@app.route('/get_mentor_image', methods=['GET'])
def get_mentor_image():
    mentor_id = request.args.get('mentor_id')  # 'mentor_name'에서 'mentor_id'로 변경

    if not mentor_id:
        return jsonify({'error': 'mentor_id 파라미터가 필요합니다.'}), 400

    # 지원하는 이미지 확장자 리스트
    extensions = ['jpg', 'jpeg', 'png', 'gif']

    # static/uploads 디렉토리 경로
    upload_folder = os.path.join(app.root_path, 'static', 'uploads')

    # 멘토 아이디와 일치하는 파일 찾기
    for ext in extensions:
        filename = f"{mentor_id}.{ext}"
        file_path = os.path.join(upload_folder, filename)
        if os.path.exists(file_path):
            # 파일이 존재하면 URL 생성
            image_url = url_for('static', filename=f'uploads/{filename}')
            return jsonify({'image_url': image_url})

    # 파일을 찾지 못한 경우
    return jsonify({'error': 'Image not found'}), 404


# 특정 클래스에 사용자가 신청할 때 호출
@app.route('/apply_class/<class_title>', methods=['POST'])
def apply_class(class_title):
    applicant_name = request.form['applicant_name']
    applicant_id = request.form['applicant_id']
    email = request.form['email']

    # applications.csv에 신청 정보 저장
    with open('static/applications.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([class_title, applicant_id, applicant_name, email, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    # MySQL에 신청 정보 저장
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # 중복 신청 확인
            check_query = """
            SELECT COUNT(*) FROM applications
            WHERE class_title = %s AND applicant_id = %s
            """
            cursor.execute(check_query, (class_title, applicant_id))
            result = cursor.fetchone()

            if result[0] > 0:
                return jsonify({"success": False, "message": "이미 신청된 클래스입니다."})

            # 신청 정보 삽입
            insert_query = """
            INSERT INTO applications (class_title, applicant_id, applicant_name, email, application_date)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (class_title, applicant_id, applicant_name, email, datetime.now()))
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"MySQL 오류: {e}")
        return jsonify({"success": False, "message": "MySQL 오류가 발생했습니다."})
    finally:
        if 'connection' in locals() and connection:
            connection.close()

    # C 함수 호출로 신청 처리
    class_title_bytes = class_title.encode('utf-8')
    success = c_function.apply_class_in_c(class_title_bytes)  # C 함수 호출

    # C 함수 호출이 성공하면 MySQL에서 current_applicants 값을 증가
    if success:
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                # current_applicants 증가
                update_query = """
                UPDATE classes
                SET current_applicants = current_applicants + 1
                WHERE class_title = %s
                """
                cursor.execute(update_query, (class_title,))
                connection.commit()
        except pymysql.MySQLError as e:
            print(f"MySQL 오류 (current_applicants 업데이트 실패): {e}")
            return jsonify({"success": False, "message": "신청 처리 중 오류가 발생했습니다."})
        finally:
            if 'connection' in locals() and connection:
                connection.close()

        return render_template('class.html', classes=load_classes_from_c(), success_message="신청이 완료되었습니다")
    else:
        return redirect(url_for('class_page', error="신청 인원이 초과되었습니다.")), 400



# ----------------------------- 정세은 ----------------------------
@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "User not logged in"}), 401

    user_info = {
        "id": user_id.decode('utf-8'),  # 바이트형식에서 문자열로 변환
    }
    return jsonify(user_info)

@app.route('/get_user_info_simple', methods=['GET'])
def get_user_info_simple():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "User not logged in"}), 401

    user_info = {
        "id": user_id.decode('utf-8'),  # 바이트형식에서 문자열로 변환
    }
    return jsonify(user_info)

@app.route('/mypage')
def mypage():
    if 'user_id' not in session:
        return render_template('login.html', message="올바르지 못한 접근입니다.")

    user_id = session['user_id'].decode('utf-8')  # 세션에서 사용자 ID 가져오기
    enrolled_classes = []

    # applications.csv에서 현재 사용자와 관련된 클래스 정보를 읽기
    try:
        with open('static/applications.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                class_title, applicant_id, applicant_name, email, apply_time = row
                if applicant_id == user_id:
                    enrolled_classes.append(class_title)
    except FileNotFoundError:
        pass  # 파일이 없으면 빈 리스트 유지

    # MySQL에서 현재 사용자와 관련된 클래스 정보를 읽기
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            query = """
            SELECT class_title 
            FROM applications 
            WHERE applicant_id = %s
            """
            cursor.execute(query, (user_id,))
            mysql_classes = cursor.fetchall()
            for mysql_class in mysql_classes:
                class_title = mysql_class[0]
                if class_title not in enrolled_classes:  # 중복 방지
                    enrolled_classes.append(class_title)
    except pymysql.MySQLError as e:
        print(f"MySQL 오류: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()

    # 모든 클래스 정보 로드 후 필터링
    all_classes = load_classes_from_c()  # 모든 클래스 정보를 로드
    filtered_classes = [
        cls for cls in all_classes if cls['class_title'] in enrolled_classes
    ]

    return render_template('mypage.html', classes=filtered_classes)


# 마이페이지-고객센터 라우트
@app.route('/help')
def help():
    return render_template('help.html')  # help.html 렌더링

# 마이페이지-프로필수정 라우트
@app.route('/picture_change')
def picture_change():
    return render_template('picture_change.html')

@app.route('/update-profile-picture', methods=['POST'])
def update_profile_picture():
    data = request.json
    photo = data.get('photo')
    user_id = session.get('user_id')  # 세션에서 사용자 ID 가져오기

    if not user_id:
        return jsonify(success=False, message="User not logged in")

    if photo:
        # 세션에 프로필 사진 경로 저장
        session['profile_pic'] = photo
        return jsonify(success=True, message="프로필 사진이 성공적으로 변경되었습니다.")
    
    return jsonify(success=False, message="사진 정보가 없습니다.")



@app.route('/get-profile-picture', methods=['GET'])
def get_profile_picture():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify(success=False, message="User not logged in")

    # 세션에서 프로필 사진 경로 가져오기
    photo = session.get('profile_pic', '/static/images/profile/default.png')  # 기본값 제공
    return jsonify(success=True, photo=photo)


@app.route('/change_id', methods=['POST'])
def change_id():
    data = request.json
    old_id = session.get('user_id')  # 세션에서 기존 ID 가져오기
    new_id = data.get('new_id')  # JSON 데이터에서 새 ID 가져오기

    # 'bytes' 객체를 'str'로 변환
    if isinstance(old_id, bytes):
        old_id = old_id.decode('utf-8')
    if isinstance(new_id, bytes):
        new_id = new_id.decode('utf-8')

    # 검증
    if not old_id or not new_id:
        return jsonify({"success": False, "message": "Invalid input"})

    try:
        # C 함수 호출
        result = c_function.change_id(old_id.encode('utf-8'), new_id.encode('utf-8'))
        if not result:
            return jsonify({"success": False, "message": "C function failed to change ID"})

        # MySQL에서 ID 변경
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                # MySQL 관련 테이블 업데이트
                related_tables = {
                    'users': 'id',
                    'applications': 'applicant_id',
                    'classes': 'mentor_id',
                    'comments': 'user_id',
                    'likes': 'user_id',
                    'community_posts': 'user_id'
                }

                for table, column in related_tables.items():
                    update_query = f"UPDATE {table} SET {column} = %s WHERE {column} = %s"
                    cursor.execute(update_query, (new_id, old_id))

                connection.commit()
                print("MySQL 데이터 업데이트 완료")
        except pymysql.MySQLError as e:
            print(f"MySQL 오류: {e}")
            return jsonify({"success": False, "message": "MySQL 업데이트 중 오류 발생"})
        finally:
            if 'connection' in locals() and connection:
                connection.close()

        # CSV 업데이트
        export_sql_csv()

        # 세션 업데이트
        session['user_id'] = new_id

        return jsonify({"success": True, "message": "ID successfully changed"})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "Unexpected error occurred"})


@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.json
    user_id = session.get('user_id')  # 세션에서 user_id 가져오기
    old_password = session.get('user_password')  # 세션에서 user_password 가져오기
    new_password = data.get('newPassword')  # JSON 데이터에서 newPassword 가져오기

    # 검증
    if not user_id or not old_password or not new_password:
        return jsonify({"success": False, "message": "Invalid input"})

    # 기존 비밀번호 확인 및 새 비밀번호 변경 (MySQL에서)
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # 기존 비밀번호 확인
            query = "SELECT id FROM users WHERE id = %s AND pw = %s"
            cursor.execute(query, (user_id, old_password))
            user_exists = cursor.fetchone()

            if not user_exists:
                return jsonify({"success": False, "message": "Invalid old password"})

            # 비밀번호 업데이트
            update_query = "UPDATE users SET pw = %s WHERE id = %s"
            cursor.execute(update_query, (new_password, user_id))
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"MySQL 오류: {e}")
        return jsonify({"success": False, "message": "Database error"})
    finally:
        if 'connection' in locals() and connection:
            connection.close()

    # 기존 C 함수 호출 유지
    result = c_function.change_password(user_id, old_password, new_password.encode('utf-8'))

    if result:
        session.pop('user_id', None)  # 세션에서 삭제 (로그아웃)
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Failed to change password"})

# -------------------------------- 우재연 --------------------------------------------
# 데이터 저장 함수 호출 (C DLL 사용)
def save_community_post(content, image_path, user_id):
    # 기존 CSV 파일 저장
    with open('static/community_posts.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 현재 시간
        writer.writerow([user_id, content, image_path, timestamp])  # 순서를 맞춤

    # MySQL 데이터 저장
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            query = """
            INSERT INTO community_posts (user_id, content, image_path, timestamp)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, content, image_path, timestamp))
            connection.commit()
            print(f"커뮤니티 게시글이 MySQL 데이터베이스에 저장되었습니다: {user_id}")
    except pymysql.MySQLError as e:
        print(f"MySQL 오류: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()


# 게시글 데이터 로드
def load_community_posts():

    # MySQL에서 게시글 로드
    posts = []
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            query = "SELECT user_id, content, image_path, timestamp FROM community_posts"
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                posts.append({
                    'user_id': row[0],
                    'content': row[1],
                    'image_path': row[2],
                    'timestamp': row[3].strftime("%Y-%m-%d %H:%M:%S")  # MySQL DATETIME 형식 처리
                })

    except pymysql.MySQLError as e:
        print(f"MySQL 오류: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()

    return posts



# 댓글 저장 함수
def save_comment(user_id, comment_text, image_path):
    # CSV 파일에 저장
    with open('static/comments.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 현재 시간
        writer.writerow([user_id, comment_text, image_path, timestamp])

    # MySQL에 저장
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # 댓글 데이터 삽입
            query = """
            INSERT INTO comments (user_id, comment_text, image_path, timestamp)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, comment_text, image_path, datetime.now()))
            connection.commit()
            print(f"MySQL에 댓글 저장: {user_id}, {comment_text}, {image_path}")
    except pymysql.MySQLError as e:
        print(f"MySQL 오류: {e}")
    except Exception as e:
        print(f"기타 오류: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()



# 특정 게시글의 댓글 로드
def load_comments(image_path):
    comments = []

    # MySQL에서 댓글 로드
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # MySQL에서 해당 image_path와 연결된 댓글 가져오기
            query = """
            SELECT user_id, comment_text, timestamp
            FROM comments
            WHERE image_path = %s
            """
            cursor.execute(query, (image_path,))
            mysql_comments = cursor.fetchall()

            # MySQL 데이터를 comments 리스트에 추가
            for comment in mysql_comments:
                comments.append({
                    'user': comment[0],       # user_id
                    'text': comment[1],       # comment_text
                    'timestamp': comment[2]   # timestamp
                })
    except pymysql.MySQLError as e:
        print(f"MySQL 오류: {e}")
    except Exception as e:
        print(f"기타 오류: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()

    return comments


# 좋아요 데이터 저장 함수
def save_like(user_id, image_path):
    # CSV 파일에 좋아요 데이터 저장
    with open('static/likes.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 현재 시간
        if isinstance(user_id, bytes):
            user_id = user_id.decode('utf-8')
        writer.writerow([user_id, image_path, timestamp])

    # MySQL에 좋아요 데이터 저장
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # 중복 좋아요 확인
            check_query = """
            SELECT COUNT(*) FROM likes
            WHERE user_id = %s AND image_path = %s
            """
            cursor.execute(check_query, (user_id, image_path))
            result = cursor.fetchone()

            if result[0] > 0:
                print("이미 좋아요를 눌렀습니다.")
                return

            # 좋아요 데이터 삽입
            insert_query = """
            INSERT INTO likes (user_id, image_path, timestamp)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, image_path, timestamp))
            connection.commit()
            print("MySQL에 좋아요 데이터를 성공적으로 저장했습니다.")
    except pymysql.MySQLError as e:
        print(f"MySQL 오류: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()



@app.route('/post/<path:image_path>')
def post_details(image_path):
    user_id = session.get('user_id')  # 로그인된 사용자 ID

    # user_id가 bytes라면 str로 변환
    if isinstance(user_id, bytes):
        user_id = user_id.decode('utf-8')

    print(f"Session User ID: {user_id}")  # 디버깅 로그

    if not user_id:
        return redirect(url_for('login'))

    # 게시글 로드
    posts = load_community_posts()
    post = next((p for p in posts if p['image_path'] == image_path), None)
    if not post:
        return "게시글을 찾을 수 없습니다.", 404

    print(f"Post User ID: {post['user_id']}, Logged-in User ID: {user_id}")  # 디버깅 로그

    # 댓글 로드
    comments = load_comments(image_path)

    # 댓글 작성자의 user가 bytes일 경우 디코딩
    for comment in comments:
        if isinstance(comment['user'], bytes):
            comment['user'] = comment['user'].decode('utf-8')
        print(f"Decoded Comment User: {comment['user']}")  # 디버깅 로그

    # 프로필 사진 URL 설정 (예: 세션에서 가져옴 또는 기본값)
    profile_pic = session.get('profile_pic', '/static/images/profile/default.png')

    # 좋아요 상태 확인
    liked = c_function.is_liked_by_user(user_id.encode('utf-8'), image_path.encode('utf-8')) if user_id else False
    print(f"Liked Status for User: {user_id}, Image Path: {image_path} = {liked}")  # 디버깅 로그

    return render_template('community_detail.html', post=post, comments=comments, liked=liked, profile_pic=profile_pic, user_id=user_id)

@app.route('/get-profile-picture-post', methods=['GET'])
def get_profile_picture_post():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify(success=False, message="User not logged in")

    # 세션에서 프로필 사진 경로 가져오기
    photo = session.get('profile_pic', 'static/images/profile/default.png')

    # 경로 앞에 '/'를 강제로 추가
    if not photo.startswith('/'):
        photo = f"/{photo}"

    # 디버깅 로그
    print(f"User ID: {user_id}, Profile Pic Path: {photo}")

    # 최종 경로 반환
    return jsonify(success=True, photo=photo)






# 게시글 추가 페이지
@app.route('/add_post', methods=['GET', 'POST'])
def add_community_post():
    user_id = session.get('user_id')  # 로그인된 사용자 ID
    if c_function.is_user_valid(user_id) == 0:
        return "게시글 작성 권한이 없습니다. 로그인 해주세요.", 403
    
    if request.method == 'POST':
        content = request.form['content']
        image = request.files['image']
        # user_id가 bytes로 되어 있을 수 있으므로, 이를 str로 변환
        if isinstance(user_id, bytes):
            user_id = user_id.decode('utf-8')
            
        filename = f'{user_id}_{image.filename}'  # 사진 이름 앞에 유저 아이디 붙임
        # 이미지 저장
        image_path = os.path.join('static', 'images/community', filename)   
        image.save(image_path)

        # C DLL을 사용하여 데이터 저장
        save_community_post(content, f'images/community/{filename}', user_id)

        # MySQL에 게시글 데이터 저장
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                # 게시글 데이터 삽입
                insert_query = """
                INSERT INTO community_posts (user_id, content, image_path, timestamp)
                VALUES (%s, %s, %s, %s)
                """
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 현재 시간
                cursor.execute(insert_query, (user_id, content, f'images/community/{filename}', timestamp))
                connection.commit()
                print("MySQL에 게시글 데이터를 성공적으로 저장했습니다.")
        except pymysql.MySQLError as e:
            print(f"MySQL 오류: {e}")
        finally:
            if 'connection' in locals() and connection:
                connection.close()

        return redirect(url_for('main'))

    return render_template('add_post.html')


@app.route('/add_comment', methods=['POST'])
def add_comment():
    user_id = session.get('user_id')  # 로그인된 사용자 ID
    
    if user_id is None or c_function.is_user_valid(user_id) == 0:
        return "로그인이 필요합니다.", 401

    comment_text = request.form['text']
    image_path = request.form['post_id']

    # comment_text가 bytes로 들어올 수 있으므로, 이를 str로 변환
    if isinstance(comment_text, bytes):
        comment_text = comment_text.decode('utf-8')

    # user_id가 bytes라면 이를 str로 변환
    if isinstance(user_id, bytes):
        user_id = user_id.decode('utf-8')

    # 댓글 저장
    save_comment(user_id, comment_text, image_path)

    return '', 200


# 좋아요 추가 라우트
@app.route('/like_post', methods=['POST'])
def like_post():
    user_id = session.get('user_id')  # 로그인된 사용자 ID
    if c_function.is_user_valid(user_id) == 0:
        return "로그인이 필요합니다.", 403

    image_path = request.form['image_path']
    save_like(user_id, image_path)
    return '', 200

# 게시글 삭제 및 관련 데이터 정리 라우트
@app.route('/delete_post/<path:image_path>', methods=['POST'])
def delete_post(image_path):
    user_id = session.get('user_id')  # 로그인된 사용자 ID
    if not user_id:
        return "로그인이 필요합니다.", 403

    try:
        # MySQL 데이터 삭제
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # 게시글 존재 여부 및 삭제 권한 확인
            check_query = """
            SELECT COUNT(*) FROM community_posts WHERE image_path = %s AND user_id = %s
            """
            cursor.execute(check_query, (image_path, user_id))
            result = cursor.fetchone()
            if result[0] == 0:
                return "삭제 권한이 없습니다.", 403

            # 게시글 삭제
            delete_post_query = """
            DELETE FROM community_posts WHERE image_path = %s AND user_id = %s
            """
            cursor.execute(delete_post_query, (image_path, user_id))

            # 댓글 삭제
            delete_comments_query = """
            DELETE FROM comments WHERE image_path = %s
            """
            cursor.execute(delete_comments_query, (image_path,))

            # 좋아요 삭제
            delete_likes_query = """
            DELETE FROM likes WHERE image_path = %s
            """
            cursor.execute(delete_likes_query, (image_path,))

            # 변경 사항 커밋
            connection.commit()
            print(f"게시글과 관련 데이터 삭제 완료: {image_path}")
            
    except pymysql.MySQLError as e:
        print(f"MySQL 오류: {e}")
        return "MySQL 작업 중 오류가 발생했습니다.", 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()

    return '', 200

#댓글 삭제
@app.route('/delete_comment', methods=['POST'])
def delete_comment():
    try:
        data = request.get_json()  # JSON 데이터를 가져옴
        comment_text = data.get('comment_text')  # 댓글 텍스트
        image_path = data.get('image_path')  # 게시글 이미지 경로
        user_id = session.get('user_id')  # 현재 로그인된 사용자 ID

        if not comment_text or not image_path or not user_id:
            return "필수 데이터가 누락되었습니다.", 400

        # MySQL에서 댓글 삭제
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                delete_query = """
                DELETE FROM comments
                WHERE user_id = %s AND image_path = %s AND comment_text = %s
                """
                cursor.execute(delete_query, (user_id, image_path, comment_text))
                connection.commit()

                if cursor.rowcount == 0:
                    return "댓글 삭제 실패: 존재하지 않는 댓글입니다.", 404
        except pymysql.MySQLError as e:
            print(f"MySQL 오류: {e}")
            return "데이터베이스 오류가 발생했습니다.", 500
        finally:
            if 'connection' in locals() and connection:
                connection.close()
        return '', 200
    except Exception as e:
        print(f"Error while deleting comment: {e}")
        return "댓글 삭제 중 오류가 발생했습니다.", 500


if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = '8080',debug=True)


