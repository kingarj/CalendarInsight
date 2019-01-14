$(document).ready(function() {

    $('.date-picker').each(function () {
        // sets the date values for every date-picker on the page
        var $datepicker = $(this),
            cur_date = ($datepicker.data('date') ? moment($datepicker.data('date'), "YYYY/MM/DD") : moment()),
            format = {
                "weekday" : ($datepicker.find('.weekday').data('format') ? $datepicker.find('.weekday').data('format') : "dddd"),
                "date" : ($datepicker.find('.date').data('format') ? $datepicker.find('.date').data('format') : "MMMM Do"),
                "year" : ($datepicker.find('.year').data('year') ? $datepicker.find('.weekday').data('format') : "YYYY")
            };

        // given a new date, updates the datepicker's visible and stored date attributes
        function updateDisplay(cur_date) {
            $datepicker.find('.date-container > .weekday').text(cur_date.format(format.weekday));
            $datepicker.find('.date-container > .date').text(cur_date.format(format.date));
            $datepicker.find('.date-container > .year').text(cur_date.format(format.year));
            $datepicker.data('date', cur_date.format('YYYY/MM/DD'));
            $datepicker.find('.input-datepicker').removeClass('show-input');
        }

        // posts the new date selected back to the analysis page
        function postDates(el_id, date_val) {
            // make the loading wheel visible
            document.getElementById("loader").style.display = "block"
            if (el_id === "1") {
                var other_date = document.getElementById("2").closest('.date-picker').innerText
            }
            else {
                var other_date = document.getElementById("1").closest('.date-picker').innerText
            }
            // build the POST data required
            var data = { "el_id": el_id, "date_val": date_val, "other_date": other_date }

            $.ajax({
                type: 'POST',
                contentType: 'application/json',
                url: 'analysis',
                dataType : 'json',
                data : JSON.stringify(data),
                success : function(result) {
                    // if we receive a result then hide the loading wheel
                    document.getElementById("loader").style.display = "none"
                    if ('fileName' in result) {
                        // data supplied was valid so display the new pie chart
                        document.getElementById("datewarning").style.display = "none"
                        document.getElementById("pieChart").style.display = "block"
                        fileName = result.fileName
                        $("#pieChart").attr('src', fileName)
                    }
                    else {
                        // data supplied was invalid so display the date warning
                        document.getElementById("datewarning").style.display = "block"
                        document.getElementById("pieChart").style.display = "none"
                    }
                },error : function(result){
                    // if the POST has failed altogether then display an alert
                    document.getElementById("loader").style.display = "none"
                    alert("Something's gone wrong. Please reload the page.");
                    console.log(result);
                }
            });
        }

        updateDisplay(cur_date);

        $datepicker.on('click', '[data-toggle="calendar"]', function(event) {
            event.preventDefault();
            $datepicker.find('.input-datepicker').toggleClass('show-input');
        });

        $datepicker.on('click', '.input-datepicker > .input-group-btn > button', function(event) {
            // once a new date is inputted, grab the new input and post it back to the page
            event.preventDefault();
            el_id = $datepicker['0'].id
            var $input = $(this).closest('.input-datepicker').find('input'),
                date_format = ($input.data('format') ? $input.data('format') : "YYYY/MM/DD");
            if (moment($input.val(), date_format).isValid()) {
               updateDisplay(moment($input.val(), date_format));
               postDates(el_id, cur_date);
            } else {
                alert('Invalid Date');
            }
        });

        $datepicker.on('click', '[data-toggle="datepicker"]', function(event) {
            // once an arrow is clicked, grab the new input and post it back to the page
            el_id = $datepicker['0'].id
            event.preventDefault();

            var cur_date = moment($(this).closest('.date-picker').data('date'), "YYYY/MM/DD"),
                date_type = ($datepicker.data('type') ? $datepicker.data('type') : "days"),
                type = ($(this).data('type') ? $(this).data('type') : "add"),
                amt = ($(this).data('amt') ? $(this).data('amt') : 1);

            if (type == "add") {
                cur_date = cur_date.add(date_type, amt);
            }else if (type == "subtract") {
                cur_date = cur_date.subtract(date_type, amt);
            }

            updateDisplay(cur_date);
            postDates(el_id, cur_date);
        });

    });
});