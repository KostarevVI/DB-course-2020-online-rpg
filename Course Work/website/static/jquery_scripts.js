$( document ).ready(function() {
    console.log( "ready!" );
    $('#persons_table').DataTable( {
    scrollY: "320px",
    scrollCollapse: true,
    paging: false,
    searching: false,
    ordering: false
    } );

    $('#user_meetups_table').DataTable( {
    lengthChange: false,
    paging: false,
    searching: false,
    ordering: false,
    orderClasses:true
    } );

    $('#person_attack_table').DataTable( {
    scrollY: "160px",
    scrollCollapse: true,
    paging: false,
    searching: false,
    ordering: false
    } );

    $('#person_defence_table').DataTable( {
    scrollY: "160px",
    scrollCollapse: true,
    paging: false,
    searching: false,
    ordering: false
    } );

    $('#inventory_person_1_table').DataTable( {
    scrollY: "245px",
    scrollCollapse: true,
    paging: false,
    searching: false,
    ordering: false
    } );

    $('#inventory_person_2_table').DataTable( {
    scrollY: "245px",
    scrollCollapse: true,
    paging: false,
    searching: false,
    ordering: false
    } );
});

//$(document).ready(function() {
//        $('#myTable').DataTable();
//
//});
//$(document).ready(function() {
//    $('#myTable').dataTable( {
//      "scrollY": "200px",
//      "scrollCollapse": true,
//      "paging": false
//      "searching": false
//      "ordering": false
//    } );
//});