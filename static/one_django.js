function price(baseUrl) {
    var form1 = document.getElementById('brands');
    var form2 = document.getElementById('form_price');
    var formSearch = document.getElementById('form_search')
    var startPrice = $('#startPrice')
    var endPrice = $('#endPrice')
    if (startPrice.val() ===null || startPrice.val() === '' && endPrice.val() ===null || endPrice.val() === ''){
        form1.submit()
    }else {
    var formData1 =form1.action +'?'+ new URLSearchParams(new FormData(form1)).toString();
    var formData2 = new URLSearchParams(new FormData(form2)).toString();
    var formData3 = new URLSearchParams(new FormData(formSearch)).toString();
    const combinedData = [formData1, formData2,formData3].filter(data => data).join('&');
    let finalUrl = `${combinedData}`;
    console.log('Final URL:', finalUrl);
    window.location.href = finalUrl;
    }
    endPrice.val().delete()

}

function Search_fild() {
    var forms1 =  $('#form_search');
    forms1.submit()
}


function add_to_product(ProductId) {
    var count = $('#count').val();
    $.get('/cart/add/',{ProductId,count}).then(rest =>{
        const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.onmouseenter = Swal.stopTimer;
            toast.onmouseleave = Swal.resumeTimer;
             }
                    });
            Toast.fire({
                icon: rest.icons,
                  title: rest.title
                        })
                            })
                            }
                            
                            
                            
function change_min_max(id,value) {
    var body = $("#order-detail-content")
    $.get('/product_shope/min-mix/',
        {id,value}
    ).then(ret =>{
        body.html(ret.body)
    })
}

function remove_product(id) {
    var body = $("#order-detail-content")
    $.get('/product_shope/remove/',{id}).then(rest =>{
        body.html(rest.body)
    })
}