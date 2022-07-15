async function connect_pressed() {
  /////////////////////////////////
  //   Check PS4 FTP connection
  /////////////////////////////////

  let status = document.getElementById("wb_uid1");
  let ip = document.getElementById("ip_field").value;
  let port = document.getElementById("port_field").value;

  status.innerHTML = "CONNECTING...";
  let respond = await eel.init_connection(ip, port)();
  if (respond[0] == false) {
    alert(respond[1]);
    status.innerHTML = "FAILED TO CONNECT";
    status.style.color = "red";
  } else {
    status.innerHTML = "CONNECTED";
    status.style.color = "green";
  }
  status.style.fontSize = "15px";
}

async function calculate_points() {
  /////////////////////////////////////////////////////
  //   calculate trophy points any time user onchange
  /////////////////////////////////////////////////////

  let bronze = parseInt(document.getElementById("user_bronze").value);
  let silver = parseInt(document.getElementById("user_silver").value);
  let gold = parseInt(document.getElementById("user_gold").value);
  let plat = parseInt(document.getElementById("user_plat").value);

  trophies = [bronze, silver, gold, plat];

  for (let index = 0; index < trophies.length; index++) {
    if (isNaN(trophies[index])) {
      trophies[index] = 0;
    }
  }

  // wait for Python to return the result
  result = await eel.get_points(trophies)();
  document.getElementById("calculator_result").value = result;
}

async function generate_data() {
  let userName = document.getElementById("users").value;

  let bronze = document.getElementById("total_bronze");
  let silver = document.getElementById("total_silver");
  let gold = document.getElementById("total_gold");
  let plat = document.getElementById("total_plat");
  let total = document.getElementById("total_trophies");

  let trophy_obj = [bronze, silver, gold, plat, total];
  let trophies = await eel.get_all_trophies()();

  for (let index = 0; index < trophies.length; index++) {
    trophy_obj[index].value = trophies[index];
  }

  let user_info = await eel.get_user_info()();
  let level = user_info[0];
  let percent = user_info[1];
  let percent_color = 100 - percent;
  let icon = user_info[2];

  document.getElementById("wb_uid8").innerHTML = level + "";
  document.getElementById("level_percentage-label").innerHTML = percent + "%";

  document.getElementById("level_percentage").style.backgroundImage =
    "linear-gradient( to left, white " +
    percent_color +
    "%, rgba(51, 147, 250, 0.845) 100%)";
}

window.onload = function () {
  app_version = 3.05;
  document.title = "My Trophies v" + app_version;
};

$(document).ready(function () {
  $("a[href*='#trophies_layout_grid']").click(function (event) {
    event.preventDefault();
    $("html, body")
      .stop()
      .animate(
        {
          scrollTop: $("#wb_trophies_layout_grid").offset().top - 88,
        },
        600,
        "easeOutCirc"
      );
  });
  $("#ip_field").validate({
    required: true,
    bootstrap: true,
    type: "custom",
    param:
      /\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b/,
    length_min: "4",
    color_text: "#000000",
    color_hint: "#00FF00",
    color_error: "#FF0000",
    color_border: "#808080",
    nohint: false,
    font_family: "Arial",
    font_size: "13px",
    position: "topleft",
    offsetx: 0,
    offsety: 0,
    effect: "none",
    error_text: "Invalid IP",
  });
  $("#ip_field").inputmask({
    alias: "ip",
  });
  $("#port_field").validate({
    required: true,
    bootstrap: true,
    type: "number",
    expr_min: ">=",
    expr_max: "",
    value_min: "0",
    value_max: "",
    length_min: "1",
    length_max: "8",
    color_text: "#000000",
    color_hint: "#00FF00",
    color_error: "#FF0000",
    color_border: "#808080",
    nohint: false,
    font_family: "Arial",
    font_size: "13px",
    position: "topleft",
    offsetx: 0,
    offsety: 0,
    effect: "none",
    error_text: "Invalid Port",
  });
  $("#level_percentage").progressbar({
    value: 0,
    change: function () {
      $("#level_percentage-label").text($(this).progressbar("value") + "%");
    },
  });
  $("#save_btn").button({
    icon: "ui-primary",
    iconPosition: "beginning",
  });
  $("#fetch_btn").button();
  $("#connect_btn").button();
});
