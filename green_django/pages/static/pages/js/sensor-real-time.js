/** Random integer  */
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

document.addEventListener("DOMContentLoaded", function (event) {
    var gg1 = new JustGage({
        id: "gg1",
        value: 50,
        min: 0,
        max: 100,
        title: "Target",
        label: "Air Temperature",
        pointer: true,
        textRenderer: function (val) {
            return val + "°C"
        }
        // onAnimationEnd: function () {
        //     console.log('f: onAnimationEnd()');
        // }
    });

    var gg2 = new JustGage({
        id: "gg2",
        value: 50,
        min: 0,
        max: 100,
        title: "Target",
        label: "Soil Temperature",
        pointer: true,
        textRenderer: function (val) {
            return val + "°C"
        }
        // onAnimationEnd: function () {
        //     console.log('f: onAnimationEnd()');
        // }
    });

    var gg3 = new JustGage({
        id: "gg3",
        value: 50,
        min: 0,
        max: 100,
        title: "Target",
        label: "Humidity",
        pointer: true,
        textRenderer: function (val) {
            return val + "%"
        }
        // onAnimationEnd: function () {
        //     console.log('f: onAnimationEnd()');
        // }
    });

    var gg4 = new JustGage({
        id: "gg4",
        value: 700,
        min: 300,
        max: 1100,
        title: "Target",
        label: "Air Pressure",
        pointer: true,
        textRenderer: function (val) {
            return val + "Pa"
        }
        // onAnimationEnd: function () {
        //     console.log('f: onAnimationEnd()');
        // }
    });

    var gg5 = new JustGage({
        id: "gg5",
        value: 50,
        min: 0,
        max: 100,
        title: "Target",
        label: "Soil Moisture",
        pointer: true,
        textRenderer: function (val) {
            return val
        }
        // onAnimationEnd: function () {
        //     console.log('f: onAnimationEnd()');
        // }
    });

    document.getElementById('gg1_refresh').addEventListener('click', function () {
        gg1.refresh(getRandomInt(0, 100));
        gg2.refresh(getRandomInt(0, 100));
        gg3.refresh(getRandomInt(0, 100));
        gg4.refresh(getRandomInt(300, 1100));
        gg5.refresh(getRandomInt(0, 100));
        return false;
    });
});
