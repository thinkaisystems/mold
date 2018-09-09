//Flot Line Chart
$(document).ready(function() {

    var offset = 0;
    plot();

    function plot() {
        var actual_anamoly = [],prediction_anamoly = [];
		var actual_anamoly_pred = [],prediction_anamoly_pred = [];
		var actual_anamoly_hist = [],prediction_anamoly_hist = [],actual_anamoly_hist_loss = [],prediction_anamoly_hist_loss_v = [];

var results_path="http://10.128.116.78:3001/data/Results/";

			
$.getJSON(results_path+"nn_pred.json", function(json) {
	//alert(json);
    
		$.each(json, function(i, field){
            //console.log(field.Actual + " " +field.Pred);
			
			 actual_anamoly_pred.push([i, field.Actual]);
            prediction_anamoly_pred.push([i, field.Pred]);
			
        });
		
		var optionsNew = {
            series: {
                lines: {
                    show: true
                },
                points: {
                    show: true
                }
            },
            grid: {
                hoverable: true //IMPORTANT! this is needed for tooltip to work
            },
            yaxis: {
                min: -1.2,
                max: 1.2
            },
            tooltip: true,
            tooltipOpts: {
                content: "'%s' of %x.1 is %y.4",
                shifts: {
                    x: -60,
                    y: 25
                }
            }
        };
		
		var plotObj = $.plot($("#flot-line-chart-pred"), [{
                data: actual_anamoly_pred,
                label: "Actual"
            }, {
                data: prediction_anamoly_pred,
                label: "Prediction"
            }],
            optionsNew);
		
		
		
		
});




$.getJSON(results_path+"nn_normal.json", function(json) {
	//alert(json);
    
		$.each(json, function(i, field){
            //console.log(field.Actual + " " +field.Pred);
			
			 actual_anamoly.push([i, field.Actual]);
            prediction_anamoly.push([i, field.Pred]);
			
        });
		
		
		
		var options = {
            series: {
                lines: {
                    show: true
                },
                points: {
                    show: true
                }
            },
            grid: {
                hoverable: true //IMPORTANT! this is needed for tooltip to work
            },
            yaxis: {
                min: -1.2,
                max: 1.2
            },
            tooltip: true,
            tooltipOpts: {
                content: "'%s' of %x.1 is %y.4",
                shifts: {
                    x: -60,
                    y: 25
                }
            }
        };
		
		
		var plotObj = $.plot($("#flot-line-chart"), [{
                data: actual_anamoly,
                label: "Actual"
            }, {
                data: prediction_anamoly,
                label: "Prediction"
            }],
            options);
		
});

			
		

		
$.getJSON(results_path+"nn_history.json", function(json) {
	//alert(json);
    
		$.each(json.acc, function(i, field){            
			 actual_anamoly_hist.push([i, field]);            			
        });
		
		$.each(json.val_acc, function(i, field){           			 
            prediction_anamoly_hist.push([i, field]);			
        });
		
		
		$.each(json.loss, function(i, field){           			 
            actual_anamoly_hist_loss.push([i, field]);			
        });
		
		$.each(json.val_loss, function(i, field){           			 
            prediction_anamoly_hist_loss_v.push([i, field]);			
        });
		
		
		
		
		var options = {
            series: {
                lines: {
                    show: true
                },
                points: {
                    show: true
                }
            },
            grid: {
                hoverable: true //IMPORTANT! this is needed for tooltip to work
            },
            yaxis: {
                min: -1.2,
                max: 1.2
            },
            tooltip: true,
            tooltipOpts: {
                content: "'%s' of %x.1 is %y.4",
                shifts: {
                    x: -60,
                    y: 25
                }
            }
        };
		
		
		var plotObj = $.plot($("#flot-line-chart-history"), [{
                data: actual_anamoly_hist,
                label: "Acc"
            }, {
                data: prediction_anamoly_hist,
                label: "Acc Val"
            }
			, {
                data: actual_anamoly_hist_loss,
                label: "Loss"
            }
			, {
                data: prediction_anamoly_hist_loss_v,
                label: "Loss Val"
            }],
            options);
		
});

		
        

        
    }
});

