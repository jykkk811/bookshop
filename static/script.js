let cart = [];

// 📌 장바구니에 책 추가
function addToCart(bookTitle, paymentMethod, originalPrice, discount) {
    let totalPrice = originalPrice - discount;
    cart.push({
        bookTitle,
        paymentMethod,
        originalPrice,
        discount,
        totalPrice
    });
    updateCart();
}

// 📌 장바구니 UI 업데이트
function updateCart() {
    let cartTable = document.getElementById("cart-table");
    cartTable.innerHTML = "";
    cart.forEach((item, index) => {
        let row = `<tr>
            <td>${item.bookTitle}</td>
            <td>${item.paymentMethod}</td>
            <td>${item.originalPrice}원</td>
            <td>${item.discount}원</td>
            <td>${item.totalPrice}원</td>
            <td><button onclick="removeFromCart(${index})">❌ 삭제</button></td>
        </tr>`;
        cartTable.innerHTML += row;
    });
}

// 📌 장바구니에서 삭제
function removeFromCart(index) {
    cart.splice(index, 1);
    updateCart();
}

// 📌 장바구니 데이터 서버로 전송 (판매 기록)
function checkout() {
    fetch("/sell", {
        method: "POST",
        body: JSON.stringify({ cart }),
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        cart = [];
        updateCart();
    })
    .catch(error => console.error("판매 기록 중 오류:", error));
}
