const $button = $("button[data-type='expence']")

function renderChart(chartData){
    var chart = am4core.create("chartDiv", am4charts.PieChart);
    chart.data = chartData ;

    var pieSeries = chart.series.push(new am4charts.PieSeries());
    pieSeries.dataFields.value = "ammount";
    pieSeries.dataFields.category = "label";

    pieSeries.labels.template.disabled = true;
    pieSeries.ticks.template.disabled = true;
}

$button.on('click',()=>{
    getChartData()
})

chartData =[];

var getChartData = () =>{
    $.get('/budget/chart',(response)=>{
        chartData = response.chart_data
        renderChart(chartData)
    })
}
    
$(document).ready(()=>{
    am4core.useTheme(am4themes_kelly);
    am4core.options.autoDispose = true;
    getChartData()

})