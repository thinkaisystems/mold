$(document).ready(function() {

    var results_path="http://"+_global_parser_hostip+":"+_global_parser_hostport+"/data/Results/";
	
$("#div-chart-canvas").find("div.panel-heading").click(function() {
  $('#div-chart-canvas').toggleClass('col-lg-6 col-lg-12'); 
  
window.myLine.resize();

});


$("#div-train-canvas").find("div.panel-heading").click(function() {
  $('#div-train-canvas').toggleClass('col-lg-6 col-lg-12');
  //window.mytrain.update();
  
   $('html, body').animate({
        scrollTop: $("#div-train-canvas").offset().top
    }, 1000);
	
	window.mytrain.resize();
	
});



			
$.getJSON(results_path+"nn_pred.json", function(json) {
	//alert(json);
    var actual_anamoly_pred = [],prediction_anamoly_pred = [], _data_pred=[],_data_actual=[],pred_labels=[];
	
		$.each(json, function(i, field){
            //console.log(field.Actual + " " +field.Pred);
			
			//actual_anamoly_pred.push([i, field.Actual]);
            //prediction_anamoly_pred.push([i, field.Pred]);
			
			_data_actual.push(field.Actual);
			_data_pred.push(field.Pred);
			pred_labels.push(i);
			
        });
		
		
	
	
	var lineChartData = {
        labels: pred_labels,
        datasets: [{
            label: "Prediction",
            borderColor: window.chartColors.blue,
            backgroundColor: window.chartColors.blue,
            fill: false,
            data:   _data_pred,
            yAxisID: "y-axis-1",
        }, {
            label: "Actual",
            borderColor: window.chartColors.red,
            backgroundColor: window.chartColors.red,
            fill: false,
            data: _data_actual,
            yAxisID: "y-axis-1"
        }]
    };
 
	
	var ctx = document.getElementById("chart-canvas").getContext("2d");
	var train = document.getElementById("train-canvas").getContext("2d");
        window.myLine = Chart.Line(ctx, {
            data: lineChartData,
            options: {
                responsive: true,
				
                hoverMode: 'index',
                stacked: false,
                title:{
                    display: true,
                    text:'Anamoly'
                },
                scales: {
                    yAxes: [{
                        type: "linear", // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                        display: true,
                        position: "left",
                        id: "y-axis-1",					
                        
                    }, 
					
					],
                }
            }
        }); 
		
	
});






$.getJSON(results_path+"nn_history.json", function(json) {
	//alert(json);
    var _data_loss = [],_data_val_loss = [], _data_acc=[],_data_val_acc=[],_hist_labels=[];
	
		$.each(json.acc, function(i, field){            
			 _data_acc.push(field);
			 _hist_labels.push(i);
        });
		
		$.each(json.val_acc, function(i, field){           			 
            _data_val_acc.push(field);			
        });
		
		
		$.each(json.loss, function(i, field){           			 
            _data_loss.push( field);			
        });
		
		$.each(json.val_loss, function(i, field){           			 
            _data_val_loss.push(field);			
        });
		
	
	var lineChartDataNew = {
        labels: _hist_labels,
        datasets: [{
            label: "Acc",
            borderColor: window.chartColors.blue,
            backgroundColor: window.chartColors.blue,
            fill: false,
            data:   _data_acc,
            yAxisID: "y-axis-1",
        },{
            label: "Val Acc",
            borderColor: window.chartColors.red,
            backgroundColor: window.chartColors.red,
            fill: false,
            data: _data_val_acc,
            yAxisID: "y-axis-1"
        }
		,{
            label: "Loss",
            borderColor: window.chartColors.yellow,
            backgroundColor: window.chartColors.yellow,
            fill: false,
            data: _data_loss,
            yAxisID: "y-axis-1"
        }
		,{
            label: "Val Loss",
            borderColor: window.chartColors.green,
            backgroundColor: window.chartColors.green,
            fill: false,
            data: _data_val_loss,
            yAxisID: "y-axis-1"
        }
		]
    };
 
	
	
	var train = document.getElementById("train-canvas").getContext("2d");        		
		window.mytrain = Chart.Line(train, {
            data: lineChartDataNew,
            options: {
                responsive: true,
                hoverMode: 'index',
                stacked: false,
                title:{
                    display: true,
                    text:'History'
                },
                scales: {
                    yAxes: [{
                        type: "linear", // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                        display: true,
                        position: "left",
                        id: "y-axis-1",					
                        
                    }, 
					
					],
                }
            }
        }); 
	
	
});




	
});