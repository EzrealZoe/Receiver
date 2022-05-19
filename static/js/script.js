
$(function(){
        $(window).on('scroll', function(){
            if($(window).scrollTop() > 100){
                $('header').removeClass('lg').addClass('sm');
            } else {
                $('header').removeClass('sm').addClass('lg');
            }
        });//主菜单的动效

        $('.to-top').toTop();//回到顶部

        $('.view-content').addClass('clearfix');//清除内容与页码出现的浮动不正常 

    });

new WOW().init(); //源自wow.min.js动画效果
