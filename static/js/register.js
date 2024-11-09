// alert("register.js加载成功")
// step1 找到获取验证码按钮。增加点击事件
    // 不过在register.html中，head中的register.js先执行，再有btn。所以我们这么解决——函数

function bindEmailCaptchaClick(){
    console.log("bindEmailCaptchaClick函数响应成功");
    $("#captcha-btn").click(function (event){
        // $this: 代表的是 当前按钮的jquery对象
        var $this = $(this);
        // "captcha-btn"在form中，我们不希望点击这个获取验证码按钮后把所有内容提交上去，所以有下面这一行
        event.preventDefault();

        var email = $("input[name='email']").val();
        // alert(email); // 用于测试
        // 向服务器发送请求
        $.ajax({
            url:"/auth/captcha/email?email="+email,
            method: "GET",
            success: function (result){
                // console.log("AJAX success:", result);
                var code = result['code'];
                if (code == 200){
                    // alert("邮箱发送成功");
                    var countdown= 60;
                    // 开始倒计时之前，取消按钮的点击事件
                    $this.off("click");
                    var timer = setInterval(function (){
                        $this.text(countdown);
                        countdown -= 1;
                        // 自己给自己发、邮箱不存在都是不会有倒计时的
                        if(countdown <= 0){
                            // 清除定时器
                            clearInterval(timer);
                            // 将按钮的文字重新修改回来
                            $this.text("获取验证码");
                            // 重新绑定点击事件
                            bindEmailCaptchaClick();
                        }
                    }, 1000)
                }else{
                    alert(result['message']);
                }
            },
            fail: function (error){
                console.log("AJAX fail:", error);
            }
        })
    });
}
// 这个函数只有在整个页面全部加载完成后才会执行，解决了上面的问题

$(function (){
    // 寻找id为"captcha-btn"的按钮
    bindEmailCaptchaClick();
})

