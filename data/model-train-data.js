$(document).ready(function() {
//console.log(fnGetUrlParameter('model-Id'));
var results_path="http://"+_global_parser_hostip+":"+_global_parser_hostport+"/data/Results/";
fnGetDashboardData();
var _g_results_data;
var _g_model_data;
var _g_lineChartData;
	
$("#spn-chart-train-hdr-toggle").click(function() {
  $('#div-chart-canvas').toggleClass('col-lg-8 col-lg-12'); 
  $('#spn-chart-train-hdr-toggle').toggleClass('glyphicon-plus glyphicon-minus'); 
  
window.historyChart.resize();

});


function fnGetDashboardData()
{
	
	var temp_modelid=fnGetUrlParameter('model-Id');
	var temp_model;



	$.getJSON("http://"+_global_parser_hostip+":"+_global_parser_hostport+"/model-api/"+temp_modelid, function(dataMdl) {
		//console.log(dataMdl.model);
		temp_model=dataMdl.model;
		
		$('#div-chart-canvas-hdr').text(temp_model.ModelName);
		
		
		$.getJSON("http://"+_global_parser_hostip+":"+_global_parser_hostport+"/results-api/"+temp_model._id, function(data) {			
				_g_results_data=data;
				_g_model_data=temp_model;
				fnBuildDashboard(data,temp_model,null);
		});
	});

				
				
				
}



function fnBuildDashboard(data,temp_model,changeResult){
	
	var main_labels=[],_data_main=[],_data_main_anamoly=[],_data_main_anamoly_list=[];
		//console.log(data.resultsList.Result);
		var temp_result=JSON.parse(data.resultsList.Result);
		
		if(null!=changeResult)
		{
			temp_result=changeResult;
		}
		
		
		var sortedData= temp_result .sort((function (a, b) { 
                              return (a.time) - (b.time) 
                            }));
	
		
		$.each(sortedData, function(i, field){
			//console.log(field[temp_model.MainField]);			
			main_labels.push((new Date(field[temp_model.TimeSeriesField])).toUTCString());			//toUTCString  toDateString
			//main_labels.push(field[temp_model.TimeSeriesField]);			
			
			
			if(field['Actual']=='YES'){
				_data_main_anamoly.push(field[temp_model.MainField]);
				_data_main.push(NaN);				
			}
			else{
				_data_main_anamoly.push(NaN);
				_data_main.push(field[temp_model.MainField]);				
			}
			
					
			
		});
			
			
			//console.log(main_labels);
			
		if(null==changeResult)
		{	
			 _g_lineChartData = {
			labels: main_labels,
			datasets: [{
			label: "Actual",
			borderColor: window.chartColors.blue,
			backgroundColor: window.chartColors.blue,
			fill: false,
			data:   _data_main,
			
			}, {
			label: "Anamoly",
			borderColor: window.chartColors.red,
			backgroundColor: window.chartColors.red,
			fill: false,
			data: _data_main_anamoly,
			
			}]
			};
			
			
			
			
		 
	
		    var ctx = document.getElementById("chart-canvas").getContext("2d");		
			window.historyChart = Chart.Line(ctx, {
				data: _g_lineChartData,
				options: {
					responsive: true,
					legend: {
						position: 'top',
					},
					title:{
						display: true,
						text:'Training'
					},
					pan: {
						enabled: false,
						mode: 'xy' 
					},
					zoom: {
						enabled: false,
						//drag: true,
						mode: 'x',
						//sensitivity: 3,
						limits: {
							max: 10,
							min: 0.5
						}
					},
					scales: {
						xAxes: [{
							scaleLabel: {display: true,labelString: temp_model.TimeSeriesField}
							
						}, ],
						yAxes: [{
							
						scaleLabel: {display: true,labelString: temp_model.MainField}						
						
						}],						
					},					
				}
			});  
			
			
		
			fnCreateInfluencingDropdowns(data,temp_model);
		}
		else{
			console.log(_data_main_anamoly.length +","+_data_main.length );
			_g_lineChartData.labels= main_labels;
			_g_lineChartData.datasets[0].data=_data_main;
			_g_lineChartData.datasets[1].data=_data_main_anamoly;			
			window.historyChart.update();
		}
	
}

function fnCreateInfluencingDropdowns(data,temp_model)
{
	var temp_inf_fields=temp_model.FieldsSelected.split(',');
	var newSelect ; 
	var newSpan ; 
	//console.log(data.resultsList[temp_inf_fields[0]])
	var drpValues=[];
	
	
	
	for(var j=0;j<temp_inf_fields.length;j++)
	{
		newSelect = $('<select class="selectpicker show-menu-arrow form-control '+temp_inf_fields[j]+'" multiple  drpType='+temp_inf_fields[j]+'    data-actions-box="true"/>'); 
		newSpan= $('<span />').addClass('folder_name').html(temp_inf_fields[j]);
		
		//console.log("data.resultsList[temp_inf_fields[j]]------------"+temp_inf_fields[j]+"----"+j+ "----"+data.resultsList[temp_inf_fields[j]]);
		//console.log("------------"+data.resultsList[temp_inf_fields[j]]);
		drpValues=(data.resultsList[temp_inf_fields[j]]).replace('[','').replace(']','').split(',');
		//drpValues=data.resultsList[temp_inf_fields[j]];
		
		//console.log('--------------------------------------------------------');
		//console.log(data.resultsList);
		
		for(var i=0;i<drpValues.length;i++)
		{
			$('<option />', {value: drpValues[i], text: drpValues[i]}).appendTo(newSelect); 
		}
		
		$('#dvTrainingBody').append(newSpan);
		$('#dvTrainingBody').append(newSelect);
		//console.log('----------------------------');
	}
	//$('.selectpicker').dropdown()
	$('.selectpicker').selectpicker();
	fnRegisterDropdownCustomEvent(_g_results_data,temp_model);
}




function fnRegisterDropdownCustomEvent(data,temp_model) {
  
  var newData={};
  $('.selectpicker').on('changed.bs.select', function (e) {
			
	//var selected = $(this).find("option:selected").val();	
	//console.log(selected);
	var drpDownList=[];
	var temp_inf_fields=temp_model.FieldsSelected.split(',');	
	
				//console.log($(this).attr('drpType'));
	for(var j=0;j<temp_inf_fields.length;j++)
	{
		//console.log($('.selectpicker'+'.'+$(this).attr('drpType')).val());
		//console.log(temp_inf_fields[j]+"------ " +$('.selectpicker'+'.'+temp_inf_fields[j]).val());
		drpDownList.push( {type:temp_inf_fields[j],value:$('.selectpicker'+'.'+temp_inf_fields[j]).val()});
		//console.log(drpDownList);
	}
	
	var changeResult=[];	
	
//console.log("drpDownList[j].value   "+(drpDownList[0].value))	;

var _dyn_filter="",_dyn_filter_arr=[];
		
	for(var j=0;j<drpDownList.length;j++)
	{
		//console.log("drpDownList[j].value   "+(drpDownList[j].value)[0]);
		
		if(drpDownList[j].value.length>0)
		{
			$.each(drpDownList[j].value, function(i, drpfield){			
				
				_dyn_filter =_dyn_filter+" field."+drpDownList[j].type+'==='+drpfield+' || ';
				
			});
			
			_dyn_filter_arr.push("("+_dyn_filter.substring(0,_dyn_filter.lastIndexOf("||"))+")");
			_dyn_filter="";
		}
		
	}
	
	
	var final_Filter="";
	
	
	$.each(_dyn_filter_arr, function(i, field){	
	   final_Filter=final_Filter+field+" || ";
	});
	//console.log(final_Filter.substring(0,final_Filter.lastIndexOf("||")));
	
	
	
	$.each(JSON.parse(data.resultsList.Result), function(i, field){			
			
			if(eval(final_Filter.substring(0,final_Filter.lastIndexOf("||"))))
			{
				changeResult.push(field);				
				
			}	
			
	});	
	
	
	console.log("changeResult  "+changeResult.length);

	
	
	
	//newData.resultsList.Result=changeResult;
	fnBuildDashboard(_g_results_data,_g_model_data,changeResult)
		//window.historyChart.resize();
   });	

  
  
}

			
			
			
			
			
			
	
});