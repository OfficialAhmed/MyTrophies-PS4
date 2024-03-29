var isFetched = false; // Allow one fetch only
var user_trophies = [0, 0, 0, 0]; //user trophy input

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
    if (respond[1].includes("Cannot")) {
      alert(respond[1]);
    }

    status.innerHTML = "CONNECTED";
    status.style.color = "green";
  }
  status.style.fontSize = "15px";
}

async function fetch_pressed() {
  let users = await eel.get_users()();
  var options = document.getElementById("users");

  /////////////////////////////////////////////////////////////////
  //               Get user names from console
  /////////////////////////////////////////////////////////////////
  if (isFetched == false) {
    option = new Option("Pick a user", (defaultSelected = true));
    options.appendChild(option);

    for (const id in users) {
      let user_name = users[id];

      option = new Option(user_name, id);
      options.appendChild(option);
    }
    isFetched = true;
  }
}

async function calculate_points() {
  ///////////////////////////////////////////////////////////////////////////////////////
  //                  calculate trophy points any time user onchange
  ///////////////////////////////////////////////////////////////////////////////////////

  let bronze = parseInt(document.getElementById("user_bronze").value);
  let silver = parseInt(document.getElementById("user_silver").value);
  let gold = parseInt(document.getElementById("user_gold").value);
  let plat = parseInt(document.getElementById("user_plat").value);

  user_trophies = [bronze, silver, gold, plat];

  for (let index = 0; index < user_trophies.length; index++) {
    if (isNaN(user_trophies[index])) {
      user_trophies[index] = 0;
    }
  }

  // wait for Python to return the result
  result = await eel.get_points(user_trophies)();
  document.getElementById("calculator_result").value = result;

  // Recalculate trophy statistics user onchange
  generate_data();
  get_levelup_trophies();
}

async function generate_data() {
  //////////////////////////////////////////////////////////////////
  //    Fetch user trophy information from Py and display them
  /////////////////////////////////////////////////////////////////

  let bronze = document.getElementById("total_bronze");
  let silver = document.getElementById("total_silver");
  let gold = document.getElementById("total_gold");
  let plat = document.getElementById("total_plat");
  let total = document.getElementById("total_trophies");

  let user_name = document.getElementById("users").value;

  let user_bronze = user_trophies[0];
  let user_silver = user_trophies[1];
  let user_gold = user_trophies[2];
  let user_plat = user_trophies[3];

  let trophies = await eel.get_all_trophies(
    user_name,
    user_bronze,
    user_silver,
    user_gold,
    user_plat
  )();

  // Display data on page
  let trophy_obj = [bronze, silver, gold, plat, total];
  for (let index = 0; index < trophies.length; index++) {
    trophy_obj[index].value = trophies[index];
  }

  let user_info = await eel.get_user_info(
    user_bronze,
    user_silver,
    user_gold,
    user_plat
  )();
  let level = user_info[0];
  let percent = user_info[1];
  let percent_color = 100 - percent;
  let icon = "img/level badge/" + user_info[2] + ".webp";

  document.getElementById("wb_uid8").innerHTML = level + "";
  document.getElementById("level_percentage-label").innerHTML = percent + "%";
  document.getElementById("level_icon").src = icon;
  document.getElementById("level_percentage").style.backgroundImage =
    "linear-gradient( to left, white " +
    percent_color +
    "%, rgba(51, 147, 250, 0.845) 100%)";

  get_levelup_trophies();
}

async function get_levelup_trophies() {
  let trophies = await eel.get_trophies_to_levelup()();
  bronze = document.getElementById("total_bronze_to_lvl_up");
  silver = document.getElementById("total_silver_to_lvl_up");
  gold = document.getElementById("total_gold_to_lvl_up");
  plat = document.getElementById("total_plat_to_lvl_up");

  let reference = [bronze, silver, gold, plat];

  for (let index = 0; index < trophies.length; index++) {
    if (trophies[index] == 0) {
      reference[index].value = 1;
    } else {
      reference[index].value = trophies[index];
    }
  }
}

async function export_file() {
  let users = document.getElementById("users");
  let user = users.options[users.selectedIndex].text;
  let status = await eel.export_file(user)();

  if (status == "success") {
    alert("FILE EXPORTED SUCCESSFULLY!");
  } else {
    alert(
      "ERROR: Something went wrong while exporting.\nErrorID: " +
        status +
        "\nPlease contact @Officialahmed0."
    );
  }
}

window.onload = function () {
  app_version = "3.12 alpha";
  document.title = "My Trophies v" + app_version;
  document.getElementById("wb_uid2").innerHTML = "My Trophies v" + app_version;

  document.getElementById("ip_field").value = "192.168.1.35";
  document.getElementById("port_field").value = 1234;
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
