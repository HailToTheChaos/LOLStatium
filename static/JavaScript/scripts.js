// ajax
function filter(year) {
        
        var season = year; // Obtén la temporada actual desde Django
        var team = $('#team-select').val();
        var player = $('#player-select').val();
        var split = $('#split-select').val();
        
        // Realiza una solicitud AJAX al servidor
        $.ajax({
            method: 'POST',
            url: '{% url "filtro" %}',
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}', // Agrega el token CSRF
                'season': season,
                'team': team,
                'player': player,
                'split': split
            },
            dataType: 'json',
            success: function(data) {
                $('#graph').html(data.html_content);
            }
        });
    }

function toggle_menu(id) {
    const menu = document.getElementById(id)

    if (menu.style.display === "none") {
        menu.style.display = "block"
    }
    else {
        menu.style.display = "none"
    }
}
