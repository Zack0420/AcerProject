<?php include('config.php');?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>宏碁碁</title>
    <!-- 引入 Bootstrap CSS 和 Font Awesome 圖標 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <!-- 自定義 CSS 樣式 -->
    <style>
        .navbar-nav .nav-link {
            white-space: nowrap;
        }
        body {
            font-family: "微軟正黑體", Arial, "蘭亭黑 - 繁", "黑體 - 繁", sans-serif;
            line-height: 1.7;
            letter-spacing: 0.1em;
            font-size: 16px;
            font-weight: normal;
            text-align: center;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
        }

        .navbar {
            position: fixed;
            top: 0;
            width: 100%;
            background-color: #333;
            color: white;
            padding: 10px 0;
            z-index: 1000; /* 確保 Nav bar 在其他內容之上 */
        }

        .navbar-nav {
            flex-direction: row;
            justify-content: center;
        }

        .navbar .nav-item {
            margin: 0 15px;
        }

        .navbar .nav-link {
            color: white;
            text-decoration: none;
        }

        .navbar .nav-link:hover {
            color: #337ab7;
        }

        .gsi-material-button {
            -moz-user-select: none;
            -webkit-user-select: none;
            -ms-user-select: none;
            -webkit-appearance: none;
            background-color: #f2f2f2;
            background-image: none;
            border: none;
            -webkit-border-radius: 4px;
            border-radius: 4px;
            -webkit-box-sizing: border-box;
            box-sizing: border-box;
            color: #1f1f1f;
            cursor: pointer;
            font-family: 'Roboto', arial, sans-serif;
            font-size: 20px;
            height: 48px;
            letter-spacing: 0.25px;
            outline: none;
            overflow: hidden;
            padding: 0 12px;
            position: relative;
            text-align: center;
            -webkit-transition: background-color .218s, border-color .218s, box-shadow .218s;
            transition: background-color .218s, border-color .218s, box-shadow .218s;
            vertical-align: middle;
            white-space: nowrap;
            width: auto;
            max-width: 400px;
            min-width: min-content;
        }

        .gsi-material-button .gsi-material-button-icon {
            height: 20px;
            margin-right: 12px;
            min-width: 20px;
            width: 20px;
        }

        .gsi-material-button .gsi-material-button-content-wrapper {
            -webkit-align-items: center;
            align-items: center;
            display: flex;
            -webkit-flex-direction: row;
            flex-direction: row;
            -webkit-flex-wrap: nowrap;
            flex-wrap: nowrap;
            height: 100%;
            justify-content: space-between;
            position: relative;
            width: 100%;
        }

        .gsi-material-button .gsi-material-button-contents {
            -webkit-flex-grow: 1;
            flex-grow: 1;
            font-family: 'Roboto', arial, sans-serif;
            font-weight: 500;
            overflow: hidden;
            text-overflow: ellipsis;
            vertical-align: top;
        }

        .gsi-material-button .gsi-material-button-state {
            -webkit-transition: opacity .218s;
            transition: opacity .218s;
            bottom: 0;
            left: 0;
            opacity: 0;
            position: absolute;
            right: 0;
            top: 0;
        }

        .gsi-material-button:disabled {
            cursor: default;
            background-color: #ffffff61;
        }

        .gsi-material-button:disabled .gsi-material-button-state {
        background- color: #1f1f1f1f;
        }

        .gsi-material-button:disabled .gsi-material-button-contents {
            opacity : 38%;
        }

        .gsi-material-button:disabled .gsi-material-button-icon {
            opacity: 38%;
        }

        .gsi-material-button:not(:disabled):active .gsi-material-button-state, 
            .gsi-material-button:not(:disabled):focus .gsi-material-button-state {
            background-color: #001d35;
            opacity: 12%;
        }

        .gsi-material-button:not(:disabled):hover {
            -webkit-box-shadow: 0 1px 2px 0 rgba(60, 64, 67, .30), 0 1px 3px 1px rgba(60, 64, 67, .15);
            box-shadow: 0 1px 2px 0 rgba(60, 64, 67, .30), 0 1px 3px 1px rgba(60, 64, 67, .15);
        }

        .gsi-material-button:not(:disabled):hover .gsi-material-button-state {
            background-color: #001d35;
            opacity: 8%;
        }


        .content {
            margin-top: 60px; /* 確保內容不被 Nav bar 遮住 */
            padding: 20px;
        }

        .pic {
            -webkit-text-size-adjust: 100%;
            -webkit-tap-highlight-color: rgba(0,0,0,0);
            font-family: "微軟正黑體", Arial, "蘭亭黑 - 繁", "黑體 - 繁", sans-serif;
            line-height: 1.7;
            letter-spacing: 0.1em;
            font-size: 16px;
            font-weight: normal;
            text-align: center;
            visibility: visible;
            color: #337ab7;
            box-sizing: border-box;
            display: block;
            width: 120px;
            height: 120px;
            border-radius: 50%;
            overflow: hidden;
            z-index: 2;
            position: relative;
            margin-bottom: 5px;
        }

        .pic img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        #footer {
            background-color: #f8f8f8;
            padding: 40px 0;
            position: relative;
        }

        #footer .box {
            margin-bottom: 20px;
        }

        #footer .title {
            font-size: 18px;
            margin-bottom: 15px;
        }

        #footer .sitemap, #footer .connect, #footer .share {
            list-style: none;
            padding: 0;
        }

        #footer .sitemap li, #footer .connect li {
            margin-bottom: 10px;
        }

        #footer .sitemap li a, #footer .connect li a, #footer .share li a {
            color: #333;
            text-decoration: none;
        }

        #footer .sitemap li a:hover, #footer .connect li a:hover, #footer .share li a:hover {
            text-decoration: underline;
        }

        #footer .share {
            display: flex;
            justify-content: space-between;
            list-style: none;
            padding: 0;
            margin: 0;
        }

        #footer .share li {
            flex: 1;
            text-align: center;
        }

        #footer .icon {
            display: inline-block;
            width: 24px;
            height: 24px;
            background-size: cover;
        }

        #footer .icon-youtube {
            background-image: url('path-to-youtube-icon.png');
        }

        #footer .icon-ig {
            background-image: url('path-to-instagram-icon.png');
        }

        #footer .icon-fb {
            background-image: url('path-to-facebook-icon.png');
        }

        #footer .line {
            border: 0;
            border-top: 1px solid #ddd;
            margin: 10px 0;
        }

        #footer .copyright {
            font-size: 14px;
            color: #777;
            margin: 10px 0;
            text-align: center;
        }


        #footer #pageTop {
            position: absolute;
            right: 20px;
            bottom: 20px;
            font-size: 14px;
            color: #777;
            cursor: pointer;
        }

    </style>
</head>
<body>
    <!-- 導航欄 -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">
                <img src="https://i.pinimg.com/564x/e2/78/e4/e278e4e41ce6eba458deb27d36aeba36.jpg" alt="宏碁碁旅遊" width="50" height="50">
                宏碁碁旅遊
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="#">關於我們</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            旅遊方案查詢
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#">國內行程</a></li>
                            <li><a class="dropdown-item" href="#">國外行程</a></li>
                            <li><a class="dropdown-item" href="#">自由行</a></li>
                        </ul>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">行程比價</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">個人行程規劃</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="member.html">會員中心</a>
                    </li>
                </ul>
                <div class="d-flex">
                    <form class="d-flex me-2" role="search">
                        <input class="form-control me-2" type="search" placeholder="關鍵字搜尋:日本自由行" aria-label="Search">
                        <button class="btn btn-outline-success" type="submit">Search</button>
                    </form>
                    <form class="d-flex ms-4">
                        <!-- Button trigger modal -->
                    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#staticBackdrop">
                    Sign In
                    </button>

                    <!-- Modal -->
                    <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="staticBackdropLabel">Modal title</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <form>
                                <div class="form-group">
                                    <input type="email" class="form-control" placeholder="Email" required>
                                </div>
                                <div class="form-group">
                                    <input type="password" class="form-control" placeholder="Password" required>
                                </div>
                                <button type="submit" class="btn btn-primary btn-block">Sign In</button>
                                
                                <button class="gsi-material-button">
                                <div class="gsi-material-button-state"></div>
                                <div class="gsi-material-button-content-wrapper">
                                    <div class="gsi-material-button-icon">
                                    <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" xmlns:xlink="http://www.w3.org/1999/xlink" style="display: block;">
                                        <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"></path>
                                        <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"></path>
                                        <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"></path>
                                        <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"></path>
                                        <path fill="none" d="M0 0h48v48H0z"></path>
                                    </svg>
                                    </div>
                                    <span class="gsi-material-button-contents">Sign in with Google</span>
                                    <span style="display: none;">Sign in with Google</span>
                                </div>
                                </button>
                                <div class="text-center mt-3">
                                    <button type="submit" class="btn btn-primary btn-block">Sign Up</button>
                                </div>
                            </form>
                        </div>
                        <!--
                        <div class="modal-footer">
                            <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Log In</button>
                            <button type="button" class="btn btn-primary">Sign Up</button>
                        </div>-->
                        </div>
                    </div>
                    </div>
                    </form>
                </div>
            </div>
        </div>
    </nav>

    <!-- 主要內容區域 -->
    <main>
        <!-- 主打旅遊行程區塊 -->
        <section class="featured-trips">
            <!-- 輪播圖片、搜索欄等 -->
            <div id="carouselExample" class="carousel slide">
                <div class="carousel-inner">
                    <picture>
                        <div class="carousel-item active">
                            <img src="https://www.relaxed.com.tw/_upload/images/2210131152350.jpg" class="d-block w-100" alt="...">
                        </div>
                        <div class="carousel-item">
                            <img src="https://www.relaxed.com.tw/_upload/images/2405060954260.jpg" class="d-block w-100" alt="...">
                        </div>
                        <div class="carousel-item">
                            <img src="https://www.relaxed.com.tw/_upload/images/2401121840430.jpg" class="d-block w-100" alt="...">
                        </div>
                    </picture>
                </div>
                <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>
            </div>
        <hr class="line">
        </section>
        <!-- 熱門目的地區塊 -->
        <h2>精選分類</h2>
        <section class="popular-destinations">
            <ul class="nav justify-content-center">
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="#">
                        日韓
                        <span class="pic">
                            <img src="https://v3-statics.mirrormedia.mg/images/20220930100229-f0b36b3f76b7409087af99360696fdd0-w1600.webP" alt="Button Image">
                        </span>
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">中國
                        <span class="pic">
                            <img src="https://www.funtime.com.tw/blog/wp-content/uploads/2017/09/128.jpg" alt="Button Image">
                        </span>
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">東南亞
                        <span class="pic">
                            <img src="https://tw.winningenglishschool.com/wp-content/uploads/shutterstock_631205246-1.jpg" alt="Button Image">
                        </span>
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">歐美澳
                        <span class="pic">
                            <img src="https://img.travel98.com/xl/P_52369_309c06696931eef70c4003a35e91c0ff_o.jpg" alt="Button Image">
                        </span>
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">台灣離島
                        <span class="pic">
                            <img src="https://img.travel98.com/xl/P_121196_a3aeeb1d8b05881c2817a0603436b319_o.jpg" alt="Button Image">
                        </span>
                    </a>
                </li>
            </ul><hr class="line">
        <section class="popular-destinations">
            <div class="container">
                <div class="row">
                    <!-- 第一排卡片 -->
                    <div class="col-md-4">
                        <div class="card">
                            <img src="https://static.lifetour.info/image/inx/spots/oversea-01-item05.webp?v=202442016" class="card-img-top" alt="...">
                            <div class="card-body">
                                <h5 class="card-title">Card title</h5>
                                <p class="card-text">Some quick example text to build on content.</p>
                                <a href="#" class="btn btn-primary">Go somewhere</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <img src="https://static.lifetour.info/image/inx/spots/oversea-01-item05.webp?v=202442016" class="card-img-top" alt="...">
                            <div class="card-body">
                                <h5 class="card-title">Card title</h5>
                                <p class="card-text">Some quick example text to build on content.</p>
                                <a href="#" class="btn btn-primary">Go somewhere</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <img src="https://static.lifetour.info/image/inx/spots/oversea-01-item05.webp?v=202442016" class="card-img-top" alt="...">
                            <div class="card-body">
                                <h5 class="card-title">Card title</h5>
                                <p class="card-text">Some quick example text to build on content.</p>
                                <a href="#" class="btn btn-primary">Go somewhere</a>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <!-- 第二排站位符卡片 -->
                    <div class="col-md-4">
                        <div class="card" aria-hidden="true">
                            <img src="https://static.lifetour.info/image/inx/spots/oversea-01-item05.webp?v=202442016" class="card-img-top" alt="...">
                            <div class="card-body">
                                <h5 class="card-title placeholder-glow">
                                    <span class="placeholder col-6"></span>
                                </h5>
                                <p class="card-text placeholder-glow">
                                    <span class="placeholder col-7"></span>
                                    <span class="placeholder col-4"></span>
                                    <span class="placeholder col-4"></span>
                                    <span class="placeholder col-6"></span>
                                    <span class="placeholder col-8"></span>
                                </p>
                                <a class="btn btn-primary disabled placeholder col-6" aria-disabled="true"></a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card" aria-hidden="true">
                            <img src="https://static.lifetour.info/image/inx/spots/oversea-01-item05.webp?v=202442016" class="card-img-top" alt="...">
                            <div class="card-body">
                                <h5 class="card-title placeholder-glow">
                                    <span class="placeholder col-6"></span>
                                </h5>
                                <p class="card-text placeholder-glow">
                                    <span class="placeholder col-7"></span>
                                    <span class="placeholder col-4"></span>
                                    <span class="placeholder col-4"></span>
                                    <span class="placeholder col-6"></span>
                                    <span class="placeholder col-8"></span>
                                </p>
                                <a class="btn btn-primary disabled placeholder col-6" aria-disabled="true"></a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card" aria-hidden="true">
                            <img src="https://static.lifetour.info/image/inx/spots/oversea-01-item05.webp?v=202442016" class="card-img-top" alt="...">
                            <div class="card-body">
                                <h5 class="card-title placeholder-glow">
                                    <span class="placeholder col-6"></span>
                                </h5>
                                <p class="card-text placeholder-glow">
                                    <span class="placeholder col-7"></span>
                                    <span class="placeholder col-4"></span>
                                    <span class="placeholder col-4"></span>
                                    <span class="placeholder col-6"></span>
                                    <span class="placeholder col-8"></span>
                                </p>
                                <a class="btn btn-primary disabled placeholder col-6" aria-disabled="true"></a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>
    <hr class="line">
    <!-- 頁尾 -->
    <footer>
        <!-- 聯絡資訊、社交媒體連結、快速連結等 -->
        <footer id="footer">
            <div class="container">
                <div class="row">
                    <div class="col-sm-2">
                        <div class="box wow fadeIn">
                            <h3 class="title">Sitemap</h3>
                            <ul class="sitemap">
                                <li><a href="brand" draggable="false">關於宏碁碁旅遊</a></li>
                                <li><a href="faq" draggable="false">常見問題</a></li>
                                <li><a href="contact" draggable="false">聯絡我們</a></li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-sm-2">
                        <div class="box wow fadeIn">
                            <ul class="sitemap">
                                <div class="col-6">
                                    <div class="p-3"></div>
                                </div>
                                <li><a href="agencies" draggable="false">合作伙伴</a></li>
                                <li><a href="/siteadmin/login.php" draggable="false">廠商專區</a></li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-sm-4">
                        <div class="box wow fadeIn">
                            <h3 class="title">Connect</h3>
                            <ul class="connect">
                                <li><a href="tel:04-36086935" draggable="false">04-123456（電話）</a></li>
                                <li><a href="javascript:;" draggable="false">04-123456（傳真）</a></li>
                                <li>
                                    <a href="https://www.google.com/maps/" class="gmap" draggable="false">聯成功館分校</a>
                                </li>
                                <li><a href="mailto:relaxcom2016@gmail.com" draggable="false">宏碁碁旅遊@gmail.com</a></li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-sm-4">
                        <div class="box wow fadeIn">
                            <h3 class="title">Follow Us</h3>
                            <ul class="share">
                                <li>
                                    <a href="https://www.youtube.com/" target="_blank" class="icon icon-youtube" draggable="false"><span class="text-hide">Youtube</span></a>
                                </li>
                                <li>
                                    <a href="https://www.instagram.com/" target="_blank" class="icon icon-ig" draggable="false"><span class="text-hide">Instagram</span></a>
                                </li>
                                <li>
                                    <a href="https://www.facebook.com/" target="_blank" class="icon icon-fb" draggable="false"><span class="text-hide">Facebook</span></a>
                                </li>
                            </ul>
                            <hr class="line">
                            <p class="copyright">© 2024 宏碁碁旅遊 All Rights Reserved.<br>Designed by
                                <a href="https://google.tw/" title="第一組" target="_blank" draggable="false">宏碁碁旅遊</a>
                            </p>
                        </div>
                    </div>

                </div>
            </div>
            <div id="pageTop" class="wow fadeIn d5">Page Top</div>
        </footer>

    <!-- 引入 Bootstrap JS 和 jQuery -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <!-- 自定義 JavaScript -->
    <script src="script.js"></script>
</body>
</html>