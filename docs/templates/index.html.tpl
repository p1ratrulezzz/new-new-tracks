<!doctype html>
<html lang="ru">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

    <title>${page['title']}</title>

    ##<meta name="description" content="Словарь с неординарными фразами, о которых мало кто слышал. Узнай новые слова и выпендрись перед тянками!">
    ##<meta name="keywords" content="словарь, сельский словарь, модные слова, современный словарь, современные слова, интересные слова${page['keywords']}">
    <meta name="robots" content="index, follow">
    <meta name="language" content="RU">
    <meta name="author" content="P1ratRuleZZZ">
    <meta name="distribution" content="global">
    <meta name="rating" content="mature">
    <meta name="generator" content="FreeMetaTagGenerator.com">
</head>
<body>
<div class="main-wrapper container">
    <div class="container-fluid">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header visually-hidden">
            <a class="navbar-brand" href="#"><a href="/"><h1>${page['title']}</h1></a></a>
        </div>
    </div>
    <div class="container row">
        <div class="col-12 col-md-1 col-sm-12">
            <nav id="dates-navigation" class="navbar navbar-fixed-left sticky-top">
                <nav class="nav navbar-dates">
                    % for item in tracks:
                        <a class="nav-link" href="#index-year-${item['year']}">${item['year']}</a>
                    % endfor
                </nav>
            </nav>
        </div>
        <div class="col-12 col-md-10 col-sm-12" data-spy="scroll" data-offset="0" data-target="#dates-navigation">
            % for year_tracks in tracks:
                <h4 id="index-year-${year_tracks['year']}">${year_tracks['year']}</h4>
                % for item in year_tracks['tracks']:
                    <div class="card mb-3">
                    <div class="row g-0">
                        <div class="col-md-2">
                            <a href="${item['href']}">
                                <img src="${item['image']}" class="img-fluid rounded-start">
                            </a>
                        </div>
                        <div class="col-md-8">
                            <div class="card-body">
                                    <h5 class="card-title">${item['artist']} - ${item['title']}</h5>

                                % if item['date_formatted']:
                                    <p class="card-text">${item['date_formatted']}</p>
                                % endif

                                % if item['spotify_track']:
                                <div class="card-text lazy-spotify-loader" data-spotify-embed="${item['spotify_track']}">
                                    <div class="spinner-border" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>
                                </div>
                                % endif
                            </div>
                        </div>
                    </div>
                </div>
                % endfor
            % endfor
        </div>
    </div>
</div>

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
<script src="/js/script.js?${buildhash}"></script>
</body>
</html>