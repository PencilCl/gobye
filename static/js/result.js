// 重置所有操作
$(function () {
    $all = $("body").html();
});
var $all;
function reset() {
    $("body").html($all);
}
// 移动一门课程
function move_one(e) {
    if ($(e).html() === "标记挂科") {
        var $tr = $(e).parent().parent();
        $tr.find("td:last").html('<a href="javascript:void(0)" onclick="move_one(this)">取消标记挂科</a>' + '<input name ="id" type="checkbox">');
        $("<tr>" + $tr.html() + "</tr>").insertBefore(".failed tbody tr:last");
        $tr.remove();
    } else if ($(e).html() === "标记公选") {
        var $tr = $(e).parent().parent();
        $tr.find("td:last").html('<a href="javascript:void(0)" onclick="move_one(this)">标记挂科</a>' + ' | ' +
            '<a href="javascript:void(0)" onclick="move_one(this)">取消标记公选</a>' + '<input name ="id" type="checkbox">');
        $("<tr>" + $tr.html() + "</tr>").insertBefore(".public-select tbody tr:last");
        $tr.remove();
    } else if ($(e).html() === "标记双修") {
        var $tr = $(e).parent().parent();
        $tr.find("td:last").html('<a href="javascript:void(0)" onclick="move_one(this)">标记挂科</a>' + ' | ' +
            '<a href="javascript:void(0)" onclick="move_one(this)">标记公选</a>' + ' | ' +
            '<a href="javascript:void(0)" onclick="move_one(this)">取消标记双修</a>' + '<input name ="id" type="checkbox">');
        $("<tr>" + $tr.html() + "</tr>").insertBefore(".double tbody tr:last");
        $tr.remove();
    } else if ($(e).html().substring(0, 2) === "取消") {
        var $tr = $(e).parent().parent();
        move_back($tr);
    }
}
// 批量撤销
function move_group(e) {
    var mode = $(e).attr("value");
    if (mode === "批量标记双修") {
        $(e).parent().parent().parent().find("input[name='id']:checked").each(function () {
            var $tr = $(this).parent().parent();
            $(this).parent().html('<a href="javascript:void(0)" onclick="move_one(this)">标记挂科</a>' + ' | ' +
                '<a href="javascript:void(0)" onclick="move_one(this)">标记公选</a>' + ' | ' +
                '<a href="javascript:void(0)" onclick="move_one(this)">取消标记双修</a>' + '<input name ="id" type="checkbox">');
            $("<tr>" + $tr.html() + "</tr>").insertBefore(".double tbody tr:last");
            $tr.remove();
        });
    } else if (mode === "批量标记公选") {
        $(e).parent().parent().parent().find("input[name='id']:checked").each(function () {
            var $tr = $(this).parent().parent();
            $tr.find("td:last").html('<a href="javascript:void(0)" onclick="move_one(this)">标记挂科</a>' + ' | ' +
                '<a href="javascript:void(0)" onclick="move_one(this)">取消标记公选</a>' + '<input name ="id" type="checkbox">');
            $("<tr>" + $tr.html() + "</tr>").insertBefore(".public-select tbody tr:last");
            $tr.remove();
        });
    } else if (mode.substring(0, 4) === "批量取消") {
        $(e).parent().parent().parent().find("input[name='id']:checked").each(function () {
            var $tr = $(this).parent().parent();
            move_back($tr);
        })
    }
}
// 使一门课程回到原位置
function move_back($tr) {
    var mode = $tr.find("td:eq(4)").html();
    if (mode === "公共必修课" || mode === "综合必修") {
        $tr.find("td:last").html('<a href="javascript:void(0)" onclick="move_one(this)">标记挂科</a>' + ' | ' +
            '<a href="javascript:void(0)" onclick="move_one(this)">标记公选</a>' + ' | ' +
            '<a href="javascript:void(0)" onclick="move_one(this)">标记双修</a>' + '<input name ="id" type="checkbox">');
        $("<tr>" + $tr.html() + "</tr>").insertBefore(".public-must tbody tr:last");
        $tr.remove();
    } else if (mode === "公共选修课") {
        $tr.find("td:last").html('<a href="javascript:void(0)" onclick="move_one(this)">标记挂科</a>' + ' | ' +
            '<a href="javascript:void(0)" onclick="move_one(this)">取消标记公选</a>' + '<input name ="id" type="checkbox">');
        $("<tr>" + $tr.html() + "</tr>").insertBefore(".public-select tbody tr:last");
        $tr.remove();
    } else if (mode === "学科专业核心课") {
        $tr.find("td:last").html('<a href="javascript:void(0)" onclick="move_one(this)">标记挂科</a>' + ' | ' +
            '<a href="javascript:void(0)" onclick="move_one(this)">标记公选</a>' + ' | ' +
            '<a href="javascript:void(0)" onclick="move_one(this)">标记双修</a>' + '<input name ="id" type="checkbox">');
        $("<tr>" + $tr.html() + "</tr>").insertBefore(".profession-must tbody tr:last");
        $tr.remove();
    } else if (mode === "学科专业选修课") {
        $tr.find("td:last").html('<a href="javascript:void(0)" onclick="move_one(this)">标记挂科</a>' + ' | ' +
            '<a href="javascript:void(0)" onclick="move_one(this)">标记公选</a>' + ' | ' +
            '<a href="javascript:void(0)" onclick="move_one(this)">标记双修</a>' + '<input name ="id" type="checkbox">');
        $("<tr>" + $tr.html() + "</tr>").insertBefore(".profession-select tbody tr:last");
        $tr.remove();
    }
}
// 计算学分总分
function calculate() {

}