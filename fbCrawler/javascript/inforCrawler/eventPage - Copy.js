/// <reference path="jquery.js" />
var lstResult = [], _status = 0;//completed
var liArray, threads = 1, countThreads = 0,url;
var defaultUrl;
//Helper start
function focusOrCreateTab(url) {
    chrome.windows.getAll({ "populate": true }, function (windows) {
        var existing_tab = null;
        for (var i in windows) {
            var tabs = windows[i].tabs;
            for (var j in tabs) {
                var tab = tabs[j];
                if (tab.url.indexOf(url) == 0) {
                    existing_tab = tab;
                    break;
                }
            }
        }
        if (existing_tab) {
            chrome.tabs.update(existing_tab.id, { "selected": true });
        } else {
            chrome.tabs.create({ "url": url, "selected": true });
        }
    });
}
function ShowCount(_count) {
    chrome.browserAction.setBadgeText({ text: _count + '' });
    chrome.browserAction.setTitle({ title: _count + '' });
}

function SaveToLocal(_lstResult, _type) {


    $('body').find('[download]').remove();
    const MIME_TYPE = 'text/plain;charset=UTF-8';
    var bb = new Blob([_lstResult.join('\n')], { type: MIME_TYPE });
    var link = document.createElement("a");
    link.textContent = "Save as csv";
    link.download = "List_Facebook_" + _type + "_" + new Date().getTime() + '.csv';
    link.href = window.URL.createObjectURL(bb);

    //window.open(link); //debug only

    document.body.appendChild(link);

    if ($('body').find('[download]').length != 0) {
        link.click();
    }


}
//Listen messsage
function completedScrape() {
    alert('Convert complete');
    _status = 0;//complete
    chrome.browserAction.setBadgeText({ text: 'off' });
    var data =JSON.stringify(lstResult);
    var url = 'data:text/json;charset=utf8,' + encodeURIComponent(data);
    window.open(url, '_blank');
    window.focus();	

    /*if (lstResult) {
        var lstMail = [];
        var lstPhone = [];
		var lstGender= [];
        for (var i = 0; i < lstResult.length; i++) {
            if (lstResult[i].email) {
                lstMail[lstMail.length] = lstResult[i].email;
            }
            if (lstResult[i].phone) {
                lstPhone[lstPhone.length] = lstResult[i].phone;
            }
			if (lstResult[i].gender) {
                lstGender[lstGender.length]=lstResult[i].gender;
			}
			
        }
        if (lstMail.length > 0) {
            SaveToLocal(lstMail, 'Email');
        }
        if (lstPhone.length > 0) {
            SaveToLocal(lstPhone, 'Phone');
        }
		if (lstGender.length > 0) {
            SaveToLocal(lstGender, 'Gender');
        }
    }*/
}
//https://m.facebook.com/profile.php?v=info&id=100002917108835&nocollections=1
function nextScrape() {
    if (_status == -1) {//stop
        countThreads++;
        if (countThreads == threads) {
            completedScrape();
        }
    } else {
        var _length = liArray.length;
        if (_length > 0) {
            var nextuid = liArray.shift();
            runScrape(nextuid, (_length == 1));
        } else {
            countThreads++;
            //console.log('count:' + countThreads + '---total:' + threads);
            if (countThreads == threads) {
                completedScrape();
            }
        }

        //chrome.browserAction.setBadgeText({ text: _length + '' });
        ShowCount(_length);
    }
}
//https://m.facebook.com/HvipPLC?v=info
//https://m.facebook.com/bui.thanh.ba.vuong?v=info
function runScrape(_id) {
    $.ajax({
        url: "https://facebook.com/" +_id,
        dataType: 'html'
    }).done(function (html) {
        var _docRoot = $(html);
        
		var defaultUrl="";
		defaultUrl=_docRoot.filter('noscript').eq(0).text();
		var n = defaultUrl.indexOf("URL=/");
		var m;
		if (defaultUrl.indexOf("profile")>0)
			{	
				n+=20;
				m=defaultUrl.indexOf("&");
				defaultUrl=defaultUrl.substring(n,m);
				url="https://m.facebook.com/profile.php?v=info&id=" + defaultUrl + "&nocollections=1";
			}
		else
			{	
				n+=5;
				m=defaultUrl.indexOf("?");
				defaultUrl=defaultUrl.substring(n,m);
				url="https://m.facebook.com/"+ defaultUrl +"?v=info&nocollections=1";
			}
		runMoreScrape(_id,defaultUrl);
    });
}
function runMoreScrape(_id,defaultUrl) {
    $.ajax({
        url: url,
        dataType: 'html'
    }).done(function (htmlnext) {
        var _doc = $(htmlnext);
            
        var defaultWorkEdu=[];
        _doc.find('.experience').each(function() {
			var value=$(this).children().eq(1).children().children().children().text();
			if ($.inArray(value, defaultWorkEdu) == -1)
			{
				defaultWorkEdu.push(value);
			}       
        });
        
        var defaultPlace=[];
        _doc.find('h4').each(function() {
			var value=$(this).text();
			if ($.inArray(value, defaultPlace) == -1)
			{
				defaultPlace.push(value);
			} 
        });
        
        var defaultPhone;
        _doc.find('span[dir="ltr"]').each(function () {
            defaultPhone = $(this).text();
        });

        var defaultAddress;
        _doc.find('div[title="Address"]').each(function () {
            defaultAddress=$(this).children().children().eq(0).children().text();
        });
        
        var defaultFacebook;
        _doc.find('div[title="Facebook"]').each(function () {
            defaultFacebook=$(this).children().children().eq(0).text();
        });
        
        var defaultEmail=[];
        _doc.find('a[href^=mailto]').each(function () {
            defaultEmail.push($(this).text());
            //if (!defaultEmail || defaultEmail.indexOf('@facebook.com') > 0) {
            //    defaultEmail = _email;
            //}
        });
        
        var defaultBirthday;
        _doc.find('div[title="Birthday"]').each(function () {
            defaultBirthday=$(this).children().children().eq(0).text();
        });
        
        var defaultGender;
        _doc.find('div[title="Gender"]').each(function () {
            defaultGender=$(this).children().children().eq(0).text();
        });
        
        var defaultInterestedIn;
        _doc.find('div[title="Interested In"]').each(function () {
            defaultInterestedIn=$(this).children().children().eq(0).text();
        });
        
        var defaultLanguages;
        _doc.find('div[title="Languages"]').each(function () {
            defaultLanguages=$(this).children().children().eq(0).text();
        });
        
        var defaultReligiousViews;
        _doc.find('div[title="Religious Views"]').each(function () {
            defaultReligiousViews=$(this).children().children().eq(0).children().text();
        });
        
        var defaultNickname;
        _doc.find('div[title="Nickname"]').each(function () {
            defaultNickname=$(this).children().children().eq(0).text();
        });
        
        var defaultRelationship;
        _doc.find("#relationship").each(function() {
            defaultRelationship=$(this).children().children().eq(1).text();
        });
        
        var defaultFamily=[];
        _doc.find("._5r7n").each(function() {
          defaultFamily.push($(this).attr("href"));
     });
        
        var defaultQuote;
        _doc.find("#quote").each(function() {
            defaultQuote=$(this).children().children().eq(1).text();
        });
        
        //https://m.facebook.com/timeline/app_collection/?collection_token=100001150323526%3A2409997254%3A96
        lstResult[lstResult.length] = {'id':_id,'workEdu':defaultWorkEdu,'place':defaultPlace, 'phone': defaultPhone,'address':defaultAddress,'facebook':defaultFacebook, 'email': defaultEmail,'birthday':defaultBirthday, 'gender':defaultGender,'interestedIn':defaultInterestedIn,'languages':defaultLanguages,'languages':defaultLanguages,'religiousViews':defaultReligiousViews,'nickName':defaultNickname,'relationship':defaultRelationship,'family':defaultFamily,'quote':defaultQuote,'url':defaultUrl};
        nextScrape();
    }).fail(function () {
        nextScrape();
    });
}

chrome.browserAction.onClicked.addListener(function () {
    if (_status == 1 && confirm('Do you want stop Convert ?')) {
        _status = -1;
    } else {
        focusOrCreateTab(chrome.extension.getURL('options.html'));
    }

});
chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        if (_status == 0) {
            if (request._method == "scrape") {
                liArray = request.data;
                threads = request.threads || 1;
                lstResult = [];
                _status = 1;//running
                countThreads = 0;
                if (liArray) {
                    sendResponse();
                    var uid;
                    for (var i = 0; i < threads; i++) {
                        uid = liArray.shift();
                        if (uid) {
                            runScrape(uid);
                        } else {
                            threads = i;
                            break;
                        }
                    }
                } else {
                    alert('Null List UID');
                }

            }
        } else {
            sendResponse(true);
        }
    });
chrome.runtime.onInstalled.addListener(function () {
    chrome.tabs.create({ "url": 'http://www.bis.ueh.edu.vn', "selected": true });
});