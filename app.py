from flask import Flask, render_template, request, jsonify
import gspread
from datetime import datetime
import os
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# 📌 1️⃣ .env 파일 로드
load_dotenv()

# 📌 2️⃣ 환경 변수에서 JSON 키 경로 불러오기
json_keyfile_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# 📌 3️⃣ Google Sheets API 설정 (환경 변수 활용)
credentials = Credentials.from_service_account_file(json_keyfile_path)
client = gspread.authorize(credentials)

# 📌 4️⃣ Google Sheets에서 데이터 가져오기
try:
    sales_sheet = client.open("판매 데이터").sheet1
    books_sheet = client.open("책 목록").sheet1
except gspread.exceptions.SpreadsheetNotFound:
    print("❌ Google Sheets 파일을 찾을 수 없습니다. 파일 이름을 확인하세요.")

# 📌 5️⃣ 책 목록 헤더 자동 추가
def ensure_books_headers():
    headers = ["책 제목", "가격", "결제 방법", "할인 금액", "할인 코드"]
    existing_headers = books_sheet.row_values(1)
    if not existing_headers:
        books_sheet.insert_row(headers, 1)

# 📌 6️⃣ 책 목록 가져오기
def get_books():
    ensure_books_headers()
    books = books_sheet.get_all_records()
    return books

# 📌 7️⃣ 책 추가 API
@app.route("/add_book", methods=["POST"])
def add_book():
    try:
        ensure_books_headers()
        data = request.get_json()
        
        new_book = [
            data["title"], data["price"], data["payment"],
            data["discount"], data["discount_code"]
        ]
        books_sheet.append_row(new_book)
        return jsonify({"message": "✅ 새 책이 추가되었습니다!"})

    except Exception as e:
        print(f"❌ 책 추가 중 오류 발생: {e}")
        return jsonify({"message": f"❌ 오류 발생: {str(e)}"}), 500

# 📌 8️⃣ 책 수정 API
@app.route("/edit_book", methods=["POST"])
def edit_book():
    try:
        ensure_books_headers()
        data = request.get_json()
        book_title = data["original_title"]
        
        books = books_sheet.get_all_records()
        for idx, book in enumerate(books, start=2):  # 2부터 시작 (헤더 제외)
            if book["책 제목"] == book_title:
                books_sheet.update(f"A{idx}:E{idx}", [[
                    data["title"], data["price"], data["payment"],
                    data["discount"], data["discount_code"]
                ]])
                return jsonify({"message": "✅ 책 정보가 수정되었습니다!"})

        return jsonify({"message": "❌ 해당 책을 찾을 수 없습니다."}), 400

    except Exception as e:
        print(f"❌ 책 수정 중 오류 발생: {e}")
        return jsonify({"message": f"❌ 오류 발생: {str(e)}"}), 500

# 📌 9️⃣ 책 삭제 API
@app.route("/delete_book", methods=["POST"])
def delete_book():
    try:
        ensure_books_headers()
        data = request.get_json()
        book_title = data["title"]
        
        books = books_sheet.get_all_records()
        for idx, book in enumerate(books, start=2):  # 2부터 시작 (헤더 제외)
            if book["책 제목"] == book_title:
                books_sheet.delete_rows(idx)
                return jsonify({"message": "✅ 책이 삭제되었습니다!"})

        return jsonify({"message": "❌ 해당 책을 찾을 수 없습니다."}), 400

    except Exception as e:
        print(f"❌ 책 삭제 중 오류 발생: {e}")
        return jsonify({"message": f"❌ 오류 발생: {str(e)}"}), 500

# 📌 🔟 장바구니 결제 API
@app.route("/checkout", methods=["POST"])
def checkout():
    try:
        data = request.get_json()
        cart_items = data.get("cart", [])
        salesperson = data.get("salesperson_name", "알 수 없음")
        sale_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not cart_items:
            return jsonify({"message": "🛑 장바구니가 비어 있습니다!"}), 400

        for item in cart_items:
            row = [
                sale_time, salesperson, item["title"], item["payment"],
                item["price"], item["discount"], item["total_price"],
                item.get("discount_code", "")
            ]
            sales_sheet.append_row(row)

        return jsonify({"message": "✅ 결제가 등록되었습니다!"})

    except Exception as e:
        print(f"❌ 결제 오류 발생: {e}")
        return jsonify({"message": f"❌ 오류 발생: {str(e)}"}), 500

# 📌 🔟 메인 페이지 (책 판매 키오스크)
@app.route("/")
def index():
    book_data = get_books()
    return render_template("index.html", book_data=book_data)

# 📌 🔟 설정 페이지 (책 목록 포함)
@app.route("/settings")
def settings():
    book_data = get_books()
    return render_template("settings.html", book_data=book_data)

# 📌 ✅ Flask 실행
if __name__ == "__main__":
    app.run(debug=True)
