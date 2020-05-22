/**
 * Nothing here yet. Add some stuff?
 */
 $(function () {
  $('[data-toggle="tooltip"]').tooltip();
  enableSearchOption();
})

$(function() {
	$("#pills-gold-tab").click(function(){
		populate_gold_data();
	});
	$("#pills-goldsub-tab").click(function(){
		populate_gold_data();
	});

	$("#select_goldk").change(function(){
		populate_gold_data();
	});

	$("#custom_gold").change(function(){
		populate_gold_data();
	});
	

	function populate_gold_data(){
		gold_carat = $( "#select_goldk option:selected" ).text();
		gold_gram = $("#gold_gram").text()
		percentage = $("#custom_gold").val()
	  	$.ajax(
	  		{
	  		url: "/gold/gold_data/"+gold_carat+"/"+gold_gram+"/"+percentage,
	  		success: function(result){

	    		dollar_0 = result[0][0]
	    		usdollar_0 = result[0][1]
	    		$("#dollar_0").text(dollar_0)
	    		$("#usdollar_0").text(usdollar_0)

	    		dollar_5 = result[1][0]
	    		usdollar_5 = result[1][1]
	    		$("#dollar_5").text(dollar_5)
	    		$("#usdollar_5").text(usdollar_5)

	    		dollar_10 = result[2][0]
	    		usdollar_10 = result[2][1]
				$("#dollar_10").text(dollar_10)
	    		$("#usdollar_10").text(usdollar_10)

	    		dollar_15 = result[3][0]
	    		usdollar_15 = result[3][1]
				$("#dollar_15").text(dollar_15)
	    		$("#usdollar_15").text(usdollar_15)

	    		gold_dollar_custom = result[4][0]
	    		gold_usdollar_custom = result[4][1]
				$("#gold_dollar_custom").text(gold_dollar_custom)
	    		$("#gold_usdollar_custom").text(gold_usdollar_custom)
	    		
	    		dollar_24k = result['24k'][0]
	    		usdollar_24k = result['24k'][1]
	    		$("#dollar_24k").text(dollar_24k)
	    		$("#usdollar_24k").text(usdollar_24k)
	  		}
	  	});
	}
})

$(function() {
	$("#pills-platinumsub-tab").click(function(){
		populate_platinum_data();
	});
	$("#custom_platinum").change(function(){
		populate_platinum_data();
	});

	function populate_platinum_data(){
		platinum_gram = $("#platinum_gram").text()
		percentage = $("#custom_platinum").val()
	  	$.ajax(
	  		{
	  		url: "/gold/platinum_data/"+platinum_gram+"/"+percentage,
	  		success: function(result){

	  			platinum_bp_thousand = result["platinum_bp"]
	  			$("#platinum_bp_thousand").text(platinum_bp_thousand);

	    		p_dollar_0 = result[0][0]
	    		p_usdollar_0 = result[0][1]
	    		$("#p_dollar_0").text(p_dollar_0)
	    		$("#p_usdollar_0").text(p_usdollar_0)

	    		p_dollar_5 = result[1][0]
	    		p_usdollar_5 = result[1][1]
	    		$("#p_dollar_5").text(p_dollar_5)
	    		$("#p_usdollar_5").text(p_usdollar_5)

	    		p_dollar_10 = result[2][0]
	    		p_usdollar_10 = result[2][1]
				$("#p_dollar_10").text(p_dollar_10)
	    		$("#p_usdollar_10").text(p_usdollar_10)

	    		p_dollar_15 = result[3][0]
	    		p_usdollar_15 = result[3][1]
				$("#p_dollar_15").text(p_dollar_15)
	    		$("#p_usdollar_15").text(p_usdollar_15)

	    		platinum_dollar_custom = result[4][0]
	    		platinum_usdollar_custom = result[4][1]
				$("#platinum_dollar_custom").text(platinum_dollar_custom)
	    		$("#platinum_usdollar_custom").text(platinum_usdollar_custom)
	    		
	    		p_dollar_1000 = result['1000'][0]
	    		p_usdollar_1000 = result['1000'][1]
	    		$("#p_dollar_1000").text(p_dollar_1000)
	    		$("#p_usdollar_1000").text(p_usdollar_1000)
	  		}
	  	});
	}
})

$(function() {
	$("#pills-silversub-tab").click(function(){
		populate_silver_data();
	});

	$("#select_silver").change(function(){
		populate_silver_data();
	});

	$("#custom_silver").change(function(){
		populate_silver_data();
	});
	

	function populate_silver_data(){
		silver_carat = $( "#select_silver option:selected" ).text();
		silver_gram = $("#silver_gram").text()
		percentage = $("#custom_silver").val()
	  	$.ajax(
	  		{
	  		url: "/gold/silver_data/"+silver_carat+"/"+silver_gram+"/"+percentage,
	  		success: function(result){

	    		s_dollar_0 = result[0][0]
	    		s_usdollar_0 = result[0][1]
	    		$("#s_dollar_0").text(s_dollar_0)
	    		$("#s_usdollar_0").text(s_usdollar_0)

	    		s_dollar_5 = result[1][0]
	    		s_usdollar_5 = result[1][1]
	    		$("#s_dollar_5").text(s_dollar_5)
	    		$("#s_usdollar_5").text(s_usdollar_5)

	    		s_dollar_10 = result[2][0]
	    		s_usdollar_10 = result[2][1]
				$("#s_dollar_10").text(s_dollar_10)
	    		$("#s_usdollar_10").text(s_usdollar_10)

	    		s_dollar_15 = result[3][0]
	    		s_usdollar_15 = result[3][1]
				$("#s_dollar_15").text(s_dollar_15)
	    		$("#s_usdollar_15").text(s_usdollar_15)

	    		silver_dollar_custom = result[4][0]
	    		silver_usdollar_custom = result[4][1]
				$("#silver_dollar_custom").text(silver_dollar_custom)
	    		$("#silver_usdollar_custom").text(silver_usdollar_custom)
	    		
	    		s_dollar_999 = result['999'][0]
	    		s_usdollar_999 = result['999'][1]
	    		$("#s_dollar_999").text(s_dollar_999)
	    		$("#s_usdollar_999").text(s_usdollar_999)
	  		}
	  	});
	}
})

$(function() {
	populate_chart();

	function populate_chart(){
		silver_carat = $( "#select_silver option:selected" ).text();
		silver_gram = $("#silver_gram").text()
		percentage = $("#custom_silver").val()
	  	$.ajax(
	  		{
	  		url: "/gold/chart_data/",
	  		success: function(result){
	  			load_chart(result)
	    	
	  		}
	  	});
	}

	function load_chart(result){
		labels = []
		data = []
		for(var i =0;i<result.length;i++){
			labels.push(result[i][0])
			data.push(result[i][1])
		}
		var ctx = document.getElementById("myAreaChart");
		var myLineChart = new Chart(ctx, {
		  type: 'line',
		  data: {
		    labels: labels,
		    datasets: [{
		      label: "Price",
		      lineTension: 0.3,
		      backgroundColor: "rgba(78, 115, 223, 0.05)",
		      borderColor: "rgba(78, 115, 223, 1)",
		      pointRadius: 3,
		      pointBackgroundColor: "rgba(78, 115, 223, 1)",
		      pointBorderColor: "rgba(78, 115, 223, 1)",
		      pointHoverRadius: 3,
		      pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
		      pointHoverBorderColor: "rgba(78, 115, 223, 1)",
		      pointHitRadius: 10,
		      pointBorderWidth: 2,
		      data: data
		    }],
		  },
		  options: {
		  	title: {
            	display: true,
            	text: 'Price Trend for Gold (Last 30 days)'
        	},
		    maintainAspectRatio: true,
		    layout: {
		      padding: {
		        left: 10,
		        right: 25,
		        top: -10,
		        bottom: 0
		      }
		    },
		    scales: {
		      xAxes: [{
		        time: {
		          unit: 'date'
		        },
		        gridLines: {
		          display: false,
		          drawBorder: false
		        },
		        ticks: {
		          maxTicksLimit: 30
		        }
		      }],
		      yAxes: [{
		        ticks: {
		          maxTicksLimit: 5,
		          padding: 10,
		          // Include a dollar sign in the ticks
		          callback: function(value, index, values) {
		            return '$' + number_format(value);
		          }
		        },
		        gridLines: {
		          color: "rgb(234, 236, 244)",
		          zeroLineColor: "rgb(234, 236, 244)",
		          drawBorder: false,
		          borderDash: [2],
		          zeroLineBorderDash: [2]
		        }
		      }],
		    },
		    legend: {
		      display: true
		    },
		    tooltips: {
		      backgroundColor: "rgb(255,255,255)",
		      bodyFontColor: "#858796",
		      titleMarginBottom: 10,
		      titleFontColor: '#6e707e',
		      titleFontSize: 14,
		      borderColor: '#dddfeb',
		      borderWidth: 1,
		      xPadding: 15,
		      yPadding: 15,
		      displayColors: false,
		      intersect: false,
		      mode: 'index',
		      caretPadding: 10,
		      callbacks: {
		        label: function(tooltipItem, chart) {
		          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
		          return datasetLabel + ': $' + number_format(tooltipItem.yLabel);
		        }
		      }
		    }
		  }
		});

	}

	function number_format(number, decimals, dec_point, thousands_sep) {
		  // *     example: number_format(1234.56, 2, ',', ' ');
		  // *     return: '1 234,56'
		  number = (number + '').replace(',', '').replace(' ', '');
		  var n = !isFinite(+number) ? 0 : +number,
		    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
		    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
		    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
		    s = '',
		    toFixedFix = function(n, prec) {
		      var k = Math.pow(10, prec);
		      return '' + Math.round(n * k) / k;
		    };
		  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
		  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
		  if (s[0].length > 3) {
		    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
		  }
		  if ((s[1] || '').length < prec) {
		    s[1] = s[1] || '';
		    s[1] += new Array(prec - s[1].length + 1).join('0');
		  }
		  return s.join(dec);
		}
})
