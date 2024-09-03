function price(baseUrl) {
    var form1 = document.getElementById('brands');
    var form2 = document.getElementById('form_price');
    var startPrice = $('#startPrice')
    var endPrice = $('#endPrice')
    if (startPrice.val() ===null || startPrice.val() === '' && endPrice.val() ===null || endPrice.val() === ''){
        form1.submit()
    }else {
    var formData1 =form1.action +'?'+ new URLSearchParams(new FormData(form1)).toString();
    var formData2 = new URLSearchParams(new FormData(form2)).toString();
    const combinedData = [formData1, formData2].filter(data => data).join('&');
    let finalUrl = `${combinedData}`;
    console.log('Final URL:', finalUrl);
    window.location.href = finalUrl;
    }
    endPrice.val().delete()

}