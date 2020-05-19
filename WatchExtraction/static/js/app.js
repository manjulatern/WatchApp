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
