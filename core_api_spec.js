var frisby = require("frisby");
var url = "http://demo.api.almighty.io/api/";
//var url = "http://localhost:8080/api/"

frisby.globalSetup({ // globalSetup is for ALL requests 
  request: {
    headers: { 'Content-Type': 'application/json' }
  }
});

//var obj = JSON.parse(SON.stringify({"fields":{"system.assignee":"me","system.creator":"me","system.description":"testing","system.state":"new","system.title":"remove"},"type":"system.userstory","version":"0"}));
var test1 = frisby.create('Ensure WI api reponds fine')
  test1.get(url + 'workitems')
  test1.expectStatus(200)
  //test1.inspectHeaders()
test1.toss()


var test2 = frisby.create('Ensure WIT api reponds fine')
  test2.get(url + 'workitemtypes')
  test2.expectStatus(200)
test2.toss()


var test3 = frisby.create('Create a WI')
  test3.post(url + 'workitems', {"fields":{"system.assignee":"me","system.creator":"me","system.description":"testing","system.state":"new","system.title":"remove"},"type":"system.userstory","version":0},{ json: true })
  test3.expectHeaderContains('Content-Type', 'application/vnd.workitem+json')
  test3.expectStatus(201)
  //test3.inspectBody()
  test3.expectJSONTypes({
    id: String,    //fails if exp type is given as string
    type: String,
    version: Number
  })
  test3.afterJSON(function(user) {
    frisby.create('Get User')
      .get(url + 'workitems/' + user.id)
      .expectStatus(200)
      //.inspectHeaders()
      .delete(url + 'workitems/' + user.id)
      .expectStatus(200)
      //.inspectHeaders()
    .toss()
  })

/*
  .afterJSON(function(user) {
      expect(1+1).toEqual(2);
    // Use data from previous result in next test 
    frisby.create('Update user')
      .put(url + 'workitems', {"fields": {"system.state":"open"}, "id": user.id})
      .expectStatus(200)
      .toss();
  })
*/	
test3.toss()

