document.addEventListener("DOMContentLoaded", function () {
    loadBooks();

    // 책 추가 폼 제출 이벤트
    document.getElementById("add-book-form").addEventListener("submit", function (event) {
        event.preventDefault(); // 기본 동작 막기

        // 입력된 값 가져오기
        let newBook = {
            title: document.getElementById("book-title").value,
            price: document.getElementById("book-price").value,
            payment: document.getElementById("book-payment").value,
            discount: document.getElementById("book-discount").value,
            discount_code: document.getElementById("book-discount-code").value
        };

        // API 호출하여 책 추가
        fetch("/add_book", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newBook)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // 성공 메시지 표시
            loadBooks(); // 책 목록 다시 불러오기
            document.getElementById("add-book-form").reset(); // 입력창 초기화
        })
        .catch(error => console.error("책 추가 중 오류:", error));
    });
});
