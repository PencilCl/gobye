calculate();
/**
 * 统计学分
 * @param  {列表} doms 需要统计的课程表下所有的tr
 * @return {float}      学分总和
 */
function sum(doms) {
    result = 0.0;
    doms.each(function() {
        tmp = parseFloat($(this).find("td").eq(5).text());
        if (tmp) {
            result += parseFloat($(this).find("td").eq(5).text());
        }
        console.log(result);
    });
    return result;
}
/**
 * 统计公共选修课文/理学分
 * @param  {列表} doms 公共选修课程表下所有的tr
 * @return {json}      文科学分arts, 理科学分science
 */
function divedeArtsAndScienceCredit(doms) {
    result = {
        "arts": 0.0,
        "science":0.0
    };
    doms.each(function() {
        type = $(this).find("td").eq(6).text();
        if (type === "文") {
            result.arts += parseFloat($(this).find("td").eq(5).text());
        } else if (type === "理") {
            result.science += parseFloat($(this).find("td").eq(5).text());
        }
    });
    return result;
}
/**
 * 计算所有课程学分
 */
function calculate() {
    publicCreditGet = sum($(".public-must tbody tr"));
    professionCreditGet = sum($(".profession-must tbody tr"));
    professionElectiveGet = sum($(".profession-select tbody tr"));
    electiveGet = divedeArtsAndScienceCredit($(".public-select tbody tr"));
    failCredit = sum($(".failed tbody tr"));
    doubleCoursesGet = sum($(".double tbody tr"));
    professionCreditNeed = plan.professionalRequired - professionCreditGet;
    publicCreditNeed = plan.publicRequired - publicCreditGet;
    doubleCoursesNeed = sum($(".double-need tbody tr"));
    $("#publicCreditGet").text(format(publicCreditGet));
    $("#professionCreditGet").text(format(professionCreditGet));
    $("#professionElectiveGet").text(format(professionElectiveGet));
    $("#electiveGetscience").text(format(electiveGet.science));
    $("#electiveGetarts").text(format(electiveGet.arts));
    $("#electiveSum").text(format(electiveGet.arts + electiveGet.science));
    $("#failCredit").text(format(failCredit));
    $("#doubleCoursesGet").text(format(doubleCoursesGet));

    $("#publicCreditNeed").text(format(publicCreditNeed));
    $("#professionCreditNeed").text(format(professionCreditNeed));
    tmp = plan["professionalElective"] - professionElectiveGet;
    $("#professionElectiveNeed").text(format(tmp<0?0.0:tmp));
    $("#doubleCoursesNeed").text(format(doubleCoursesNeed));

    electiveNeed = {};
    tmp = plan.artsStream - electiveGet.arts;
    electiveNeed.arts = (tmp<0?0.0:tmp);
    tmp = plan.scienceStream - electiveGet.science
    electiveNeed.science = (tmp<0?0.0:tmp);
    tmp = plan.elective - professionElectiveGet - electiveGet.arts - electiveGet.science;
    electiveNeedSum = tmp<0?(electiveNeed.arts + electiveNeed.science + professionElectiveNeed):tmp
    $("#electiveNeedarts").text(format(electiveNeed.arts));
    $("#electiveNeedscience").text(format(electiveNeed.science));
    $("#electiveNeedSum").text(format(electiveNeedSum));

    $("#totalNeed").text(format(publicCreditNeed + professionCreditNeed + electiveNeedSum + doubleCoursesNeed));
}
/**
 * 格式化学分，保留一位小数
 * @param  {float} credit 学分
 * @return {string}        格式化后的学分
 */
function format(credit) {
    credit = credit + "";
    if (credit.indexOf(".") == -1) {
        credit += ".0";
    }
    return credit;
}