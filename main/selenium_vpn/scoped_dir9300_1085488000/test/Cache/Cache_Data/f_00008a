
function dv_rolloutManager(handlersDefsArray, baseHandler) {
    this.handle = function () {
        var errorsArr = [];

        var handler = chooseEvaluationHandler(handlersDefsArray);
        if (handler) {
            var errorObj = handleSpecificHandler(handler);
            if (errorObj === null) {
                return errorsArr;
            }
            else {
                var debugInfo = handler.onFailure();
                if (debugInfo) {
                    for (var key in debugInfo) {
                        if (debugInfo.hasOwnProperty(key)) {
                            if (debugInfo[key] !== undefined || debugInfo[key] !== null) {
                                errorObj[key] = encodeURIComponent(debugInfo[key]);
                            }
                        }
                    }
                }
                errorsArr.push(errorObj);
            }
        }

        var errorObjHandler = handleSpecificHandler(baseHandler);
        if (errorObjHandler) {
            errorObjHandler['dvp_isLostImp'] = 1;
            errorsArr.push(errorObjHandler);
        }
        return errorsArr;
    };

    function handleSpecificHandler(handler) {
        var request;
        var errorObj = null;

        try {
            request = handler.createRequest();
            if (request && !request.isSev1) {
                var url = request.url || request;
                if (url) {
                    if (!handler.sendRequest(url)) {
                        errorObj = createAndGetError('sendRequest failed.',
                            url,
                            handler.getVersion(),
                            handler.getVersionParamName(),
                            handler.dv_script);
                    }
                } else {
                    errorObj = createAndGetError('createRequest failed.',
                        url,
                        handler.getVersion(),
                        handler.getVersionParamName(),
                        handler.dv_script,
                        handler.dvScripts,
                        handler.dvStep,
                        handler.dvOther
                    );
                }
            }
        }
        catch (e) {
            errorObj = createAndGetError(e.name + ': ' + e.message, request ? (request.url || request) : null, handler.getVersion(), handler.getVersionParamName(), (handler ? handler.dv_script : null));
        }

        return errorObj;
    }

    function createAndGetError(error, url, ver, versionParamName, dv_script, dvScripts, dvStep, dvOther) {
        var errorObj = {};
        errorObj[versionParamName] = ver;
        errorObj['dvp_jsErrMsg'] = encodeURIComponent(error);
        if (dv_script && dv_script.parentElement && dv_script.parentElement.tagName && dv_script.parentElement.tagName == 'HEAD') {
            errorObj['dvp_isOnHead'] = '1';
        }
        if (url) {
            errorObj['dvp_jsErrUrl'] = url;
        }
        if (dvScripts) {
            var dvScriptsResult = '';
            for (var id in dvScripts) {
                if (dvScripts[id] && dvScripts[id].src) {
                    dvScriptsResult += encodeURIComponent(dvScripts[id].src) + ":" + dvScripts[id].isContain + ",";
                }
            }
            
            
            
        }
        return errorObj;
    }

    function chooseEvaluationHandler(handlersArray) {
        var config = window._dv_win.dv_config;
        var index = 0;
        var isEvaluationVersionChosen = false;
        if (config.handlerVersionSpecific) {
            for (var i = 0; i < handlersArray.length; i++) {
                if (handlersArray[i].handler.getVersion() == config.handlerVersionSpecific) {
                    isEvaluationVersionChosen = true;
                    index = i;
                    break;
                }
            }
        }
        else if (config.handlerVersionByTimeIntervalMinutes) {
            var date = config.handlerVersionByTimeInputDate || new Date();
            var hour = date.getUTCHours();
            var minutes = date.getUTCMinutes();
            index = Math.floor(((hour * 60) + minutes) / config.handlerVersionByTimeIntervalMinutes) % (handlersArray.length + 1);
            if (index != handlersArray.length) { 
                isEvaluationVersionChosen = true;
            }
        }
        else {
            var rand = config.handlerVersionRandom || (Math.random() * 100);
            for (var i = 0; i < handlersArray.length; i++) {
                if (rand >= handlersArray[i].minRate && rand < handlersArray[i].maxRate) {
                    isEvaluationVersionChosen = true;
                    index = i;
                    break;
                }
            }
        }

        if (isEvaluationVersionChosen == true && handlersArray[index].handler.isApplicable()) {
            return handlersArray[index].handler;
        }
        else {
            return null;
        }
    }
}

function doesBrowserSupportHTML5Push() {
    "use strict";
    return typeof window.parent.postMessage === 'function' && window.JSON;
}

function dv_GetParam(url, name, checkFromStart) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regexS = (checkFromStart ? "(?:\\?|&|^)" : "[\\?&]") + name + "=([^&#]*)";
    var regex = new RegExp(regexS, 'i');
    var results = regex.exec(url);
    if (results == null)
        return null;
    else
        return results[1];
}

function dv_Contains(array, obj) {
    var i = array.length;
    while (i--) {
        if (array[i] === obj) {
            return true;
        }
    }
    return false;
}

function dv_GetDynamicParams(url, prefix) {
    try {
        prefix = (prefix != undefined && prefix != null) ? prefix : 'dvp';
        var regex = new RegExp("[\\?&](" + prefix + "_[^&]*=[^&#]*)", "gi");
        var dvParams = regex.exec(url);

        var results = [];
        while (dvParams != null) {
            results.push(dvParams[1]);
            dvParams = regex.exec(url);
        }
        return results;
    }
    catch (e) {
        return [];
    }
}

function dv_createIframe() {
    var iframe;
    if (document.createElement && (iframe = document.createElement('iframe'))) {
        iframe.name = iframe.id = 'iframe_' + Math.floor((Math.random() + "") * 1000000000000);
        iframe.width = 0;
        iframe.height = 0;
        iframe.style.display = 'none';
        iframe.src = 'about:blank';
    }

    return iframe;
}

function dv_GetRnd() {
    return ((new Date()).getTime() + "" + Math.floor(Math.random() * 1000000)).substr(0, 16);
}

function dv_SendErrorImp(serverUrl, errorsArr) {

    for (var j = 0; j < errorsArr.length; j++) {
        var errorObj = errorsArr[j];
        var errorImp =   dv_CreateAndGetErrorImp(serverUrl, errorObj);
        dv_sendImgImp(errorImp);
    }
}

function dv_CreateAndGetErrorImp(serverUrl, errorObj) {
    var errorQueryString = '';
    for (key in errorObj) {
        if (errorObj.hasOwnProperty(key)) {
            if (key.indexOf('dvp_jsErrUrl') == -1) {
                errorQueryString += '&' + key + '=' + errorObj[key];
            }
            else {
                var params = ['ctx', 'cmp', 'plc', 'sid'];
                for (var i = 0; i < params.length; i++) {
                    var pvalue = dv_GetParam(errorObj[key], params[i]);
                    if (pvalue) {
                        errorQueryString += '&dvp_js' + params[i] + '=' + pvalue;
                    }
                }
            }
        }
    }

    var sslFlag = '&ssl=1';
    var errorImp = 'https://' + serverUrl + sslFlag + errorQueryString;

    return errorImp;
}

function dv_getDVUniqueKey(elm) {
    return elm && elm.getAttribute('data-uk');
}

function dv_getDVErrorGlobalScope(elm) {
    var uniqueKey = dv_getDVUniqueKey(elm);
    return uniqueKey && window._dv_win && window._dv_win[uniqueKey] && window._dv_win[uniqueKey].globalScopeVerifyErrorHandler || {};
}

function dv_onLoad(evt) {
    var elm = evt && evt.target || {};
    var globalScope = dv_getDVErrorGlobalScope(elm);
    if (globalScope) {
        var scriptSRC = dv_getScriptSRC(elm);
        if (!globalScope.isJSONPCalled) {
            setTimeout(function onTimeout(){
                globalScope.onTimeout(scriptSRC);
            }, globalScope.msTillJSONPCalled);
        }
    }
}

function dv_onResponse(evt) {
    var elm = evt && evt.target || {};
    var globalScope = dv_getDVErrorGlobalScope(elm);
    if (globalScope) {
        var scriptSRC = dv_getScriptSRC(elm);
        if (!globalScope.isJSONPCalled) {
            globalScope.onResponse(scriptSRC);
        }
    }
}

function dv_getScriptSRC(elm) {
    return elm && elm.src || '';
}
var IQPAParams = [
    "auprice", "ppid", "audeal", "auevent", "auadv", "aucmp", "aucrtv", "auorder", "ausite", "auplc", "auxch", "audvc", "aulitem",
    "auadid", "pltfrm", "aufilter1", "aufilter2", "autt", "auip", "aubndl", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9",
    "c10", "c11", "c12", "c13", "c14", "c15"
];

function dv_AppendIQPAParams(src) {
    var qs = [];
    var paramVal;
    IQPAParams.forEach(function forEachParam(paramName){
        paramVal = dv_GetParam(src, paramName);
        if (paramVal !== '' && paramVal !== null) {
            qs.push([paramName, paramVal].join('='));
        }
    });
    return qs.length && '&' + qs.join('&') || '';
}

function dv_onError(evt) {
    var elm = evt && evt.target || {};
    var globalScope = dv_getDVErrorGlobalScope(elm);
    if (globalScope) {
        globalScope.onError(dv_getScriptSRC(elm));
    }
}

function dv_getDVBSErrAddress(config) {
    return config && config.bsErrAddress || 'rtb0.doubleverify.com';
}

function dv_sendImgImp(url) {
    (new Image()).src = url;
}

function dv_sendScriptRequest(url, onLoad, onError, uniqueKey) {
    var emptyFunction = function(){};
    onLoad = onLoad || emptyFunction;
    onError = onError || emptyFunction;
    document.write('<scr' + 'ipt data-uk="' + uniqueKey + '" onerror="(' + onError + ')({target:this});" onload="(' + onLoad + ')({target:this});" type="text/javascript" src="' + url + '"></scr' + 'ipt>');
}

function dv_getPropSafe(obj, propName) {
    try {
        if (obj)
            return obj[propName];
    } catch (e) {
    }
}

function dvBsType() {
    var that = this;
    var eventsForDispatch = {};

    this.getEventsForDispatch = function getEventsForDispatch () {
        return eventsForDispatch;
    };

    var messageEventListener = function (event) {
        try {
            var timeCalled = getCurrentTime();
            var data = window.JSON.parse(event.data);
            if (!data.action) {
                data = window.JSON.parse(data);
            }
            if (data.timeStampCollection) {
                data.timeStampCollection.push({messageEventListenerCalled: timeCalled});
            }
            var myUID;
            var visitJSHasBeenCalledForThisTag = false;
            if ($dvbs.tags) {
                for (var uid in $dvbs.tags) {
                    if ($dvbs.tags.hasOwnProperty(uid) && $dvbs.tags[uid] && $dvbs.tags[uid].t2tIframeId === data.iFrameId) {
                        myUID = uid;
                        visitJSHasBeenCalledForThisTag = true;
                        break;
                    }
                }
            }

        } catch (e) {
            try {
                dv_SendErrorImp(window._dv_win.dv_config.tpsErrAddress + '/visit.jpg?ctx=818052&cmp=1619415&dvtagver=6.1.src&jsver=0&dvp_ist2tListener=1', {dvp_jsErrMsg: encodeURIComponent(e)});
            } catch (ex) {
            }
        }
    };

    if (window.addEventListener)
        addEventListener("message", messageEventListener, false);
    else
        attachEvent("onmessage", messageEventListener);

    this.pubSub = new function () {

        var subscribers = [];

        this.subscribe = function (eventName, uid, actionName, func) {
            if (!subscribers[eventName + uid])
                subscribers[eventName + uid] = [];
            subscribers[eventName + uid].push({Func: func, ActionName: actionName});
        };

        this.publish = function (eventName, uid) {
            var actionsResults = [];
            if (eventName && uid && subscribers[eventName + uid] instanceof Array)
                for (var i = 0; i < subscribers[eventName + uid].length; i++) {
                    var funcObject = subscribers[eventName + uid][i];
                    if (funcObject && funcObject.Func && typeof funcObject.Func == "function" && funcObject.ActionName) {
                        var isSucceeded = runSafely(function () {
                            return funcObject.Func(uid);
                        });
                        actionsResults.push(encodeURIComponent(funcObject.ActionName) + '=' + (isSucceeded ? '1' : '0'));
                    }
                }
            return actionsResults.join('&');
        };
    };

    this.domUtilities = new function () {

        this.addImage = function (url, parentElement, trackingPixelCompleteCallbackName) {
            url = appendCacheBuster(url);
            if (typeof(navigator.sendBeacon) === 'function') {
                var isSuccessfullyQueuedDataForTransfer = navigator.sendBeacon(url);
                if (isSuccessfullyQueuedDataForTransfer && typeof(window[trackingPixelCompleteCallbackName]) === 'function') {
                    window[trackingPixelCompleteCallbackName]();
                }
                return;
            }

            var image = new Image();
            if (typeof(window[trackingPixelCompleteCallbackName]) === 'function') {
                image.addEventListener('load', window[trackingPixelCompleteCallbackName]);
            }
            image.src = url;
        };

        this.addScriptResource = function (url, parentElement, onLoad, onError, uniqueKey) {
            var emptyFunction = function(){};
            onLoad = onLoad || emptyFunction;
            onError = onError || emptyFunction;
            uniqueKey = uniqueKey || '';
            if (parentElement) {
                var scriptElem = parentElement.ownerDocument.createElement("script");
                scriptElem.onerror = onError;
                scriptElem.onload = onLoad;
                if (scriptElem && typeof(scriptElem.setAttribute) === 'function') {
                    scriptElem.setAttribute('data-uk', uniqueKey);
                }
                scriptElem.type = 'text/javascript';
                scriptElem.src = appendCacheBuster(url);
                parentElement.insertBefore(scriptElem, parentElement.firstChild);
            }
            else {
                addScriptResourceFallBack(url, onLoad, onError, uniqueKey);
            }
        };

        function addScriptResourceFallBack(url, onLoad, onError, uniqueKey) {
            var emptyFunction = function(){};
            onLoad = onLoad || emptyFunction;
            onError = onError || emptyFunction;
            uniqueKey = uniqueKey || '';
            var scriptElem = document.createElement('script');
            scriptElem.onerror = onError;
            scriptElem.onload = onLoad;
            if (scriptElem && typeof(scriptElem.setAttribute) === 'function') {
                scriptElem.setAttribute('data-uk', uniqueKey);
            }
            scriptElem.type = "text/javascript";
            scriptElem.src = appendCacheBuster(url);
            var firstScript = document.getElementsByTagName('script')[0];
            firstScript.parentNode.insertBefore(scriptElem, firstScript);
        }

        this.addScriptCode = function (srcCode, parentElement) {
            var scriptElem = parentElement.ownerDocument.createElement("script");
            scriptElem.type = 'text/javascript';
            scriptElem.innerHTML = srcCode;
            parentElement.insertBefore(scriptElem, parentElement.firstChild);
        };

        this.addHtml = function (srcHtml, parentElement) {
            var divElem = parentElement.ownerDocument.createElement("div");
            divElem.style = "display: inline";
            divElem.innerHTML = srcHtml;
            parentElement.insertBefore(divElem, parentElement.firstChild);
        };
    };

    this.resolveMacros = function (str, tag) {
        var viewabilityData = tag.getViewabilityData();
        var viewabilityBuckets = viewabilityData && viewabilityData.buckets ? viewabilityData.buckets : {};
        var upperCaseObj = objectsToUpperCase(tag, viewabilityData, viewabilityBuckets);
        var newStr = str.replace('[DV_PROTOCOL]', upperCaseObj.DV_PROTOCOL);
        newStr = newStr.replace('[PROTOCOL]', upperCaseObj.PROTOCOL);
        newStr = newStr.replace(/\[(.*?)\]/g, function (match, p1) {
            var value = upperCaseObj[p1];
            if (value === undefined || value === null)
                value = '[' + p1 + ']';
            return encodeURIComponent(value);
        });
        return newStr;
    };

    this.settings = new function () {
    };

    this.tagsType = function () {
    };

    this.tagsPrototype = function () {
        this.add = function (tagKey, obj) {
            if (!that.tags[tagKey])
                that.tags[tagKey] = new that.tag();
            for (var key in obj)
                that.tags[tagKey][key] = obj[key];
        };
    };

    this.tagsType.prototype = new this.tagsPrototype();
    this.tagsType.prototype.constructor = this.tags;
    this.tags = new this.tagsType();

    this.tag = function () {
    };
    this.tagPrototype = function () {
        this.set = function (obj) {
            for (var key in obj)
                this[key] = obj[key];
        };

        this.getViewabilityData = function () {
        };
    };

    this.tag.prototype = new this.tagPrototype();
    this.tag.prototype.constructor = this.tag;

    this.getTagObjectByService = function (serviceName) {

        for (var impressionId in this.tags) {
            if (typeof this.tags[impressionId] === 'object'
                && this.tags[impressionId].services
                && this.tags[impressionId].services[serviceName]
                && !this.tags[impressionId].services[serviceName].isProcessed) {
                this.tags[impressionId].services[serviceName].isProcessed = true;
                return this.tags[impressionId];
            }
        }


        return null;
    };

    this.addService = function (impressionId, serviceName, paramsObject) {

        if (!impressionId || !serviceName)
            return;

        if (!this.tags[impressionId])
            return;
        else {
            if (!this.tags[impressionId].services)
                this.tags[impressionId].services = {};

            this.tags[impressionId].services[serviceName] = {
                params: paramsObject,
                isProcessed: false
            };
        }
    };

    this.Enums = {
        BrowserId: {Others: 0, IE: 1, Firefox: 2, Chrome: 3, Opera: 4, Safari: 5},
        TrafficScenario: {OnPage: 1, SameDomain: 2, CrossDomain: 128}
    };

    this.CommonData = {};

    var runSafely = function (action) {
        try {
            var ret = action();
            return ret !== undefined ? ret : true;
        } catch (e) {
            return false;
        }
    };

    var objectsToUpperCase = function () {
        var upperCaseObj = {};
        for (var i = 0; i < arguments.length; i++) {
            var obj = arguments[i];
            for (var key in obj) {
                if (obj.hasOwnProperty(key)) {
                    upperCaseObj[key.toUpperCase()] = obj[key];
                }
            }
        }
        return upperCaseObj;
    };

    var appendCacheBuster = function (url) {
        if (url !== undefined && url !== null && url.match("^http") == "http") {
            if (url.indexOf('?') !== -1) {
                if (url.slice(-1) == '&')
                    url += 'cbust=' + dv_GetRnd();
                else
                    url += '&cbust=' + dv_GetRnd();
            }
            else
                url += '?cbust=' + dv_GetRnd();
        }
        return url;
    };

    
    var messagesClass = function () {
        var waitingMessages = [];

        this.registerMsg = function(dvFrame, data) {
            if (!waitingMessages[dvFrame.$frmId]) {
                waitingMessages[dvFrame.$frmId] = [];
            }

            waitingMessages[dvFrame.$frmId].push(data);

            if (dvFrame.$uid) {
                sendWaitingEventsForFrame(dvFrame, dvFrame.$uid);
            }
        };

        this.startSendingEvents = function(dvFrame, impID) {
            sendWaitingEventsForFrame(dvFrame, impID);
            
        };

        function sendWaitingEventsForFrame(dvFrame, impID) {
            if (waitingMessages[dvFrame.$frmId]) {
                var eventObject = {};
                for (var i = 0; i < waitingMessages[dvFrame.$frmId].length; i++) {
                    var obj = waitingMessages[dvFrame.$frmId].pop();
                    for (var key in obj) {
                        if (typeof obj[key] !== 'function' && obj.hasOwnProperty(key)) {
                            eventObject[key] = obj[key];
                        }
                    }
                }
                that.registerEventCall(impID, eventObject);
            }
        }

        function startMessageManager() {
            for (var frm in waitingMessages) {
                if (frm && frm.$uid) {
                    sendWaitingEventsForFrame(frm, frm.$uid);
                }
            }
            setTimeout(startMessageManager, 10);
        }
    };
    this.messages = new messagesClass();

    this.dispatchRegisteredEventsFromAllTags = function () {
        for (var impressionId in this.tags) {
            if (typeof this.tags[impressionId] !== 'function' && typeof this.tags[impressionId] !== 'undefined')
                dispatchEventCalls(impressionId, this);
        }
    };

    var dispatchEventCalls = function (impressionId, dvObj) {
        var tag = dvObj.tags[impressionId];
        var eventObj = eventsForDispatch[impressionId];
        if (typeof eventObj !== 'undefined' && eventObj != null) {
            var url = 'https://' + tag.ServerPublicDns + "/bsevent.gif?impid=" + impressionId + '&' + createQueryStringParams(eventObj);
            dvObj.domUtilities.addImage(url, tag.tagElement.parentElement);
            eventsForDispatch[impressionId] = null;
        }
    };

    this.registerEventCall = function (impressionId, eventObject, timeoutMs) {
        addEventCallForDispatch(impressionId, eventObject);

        if (typeof timeoutMs === 'undefined' || timeoutMs == 0 || isNaN(timeoutMs))
            dispatchEventCallsNow(this, impressionId, eventObject);
        else {
            if (timeoutMs > 2000)
                timeoutMs = 2000;

            var dvObj = this;
            setTimeout(function () {
                dispatchEventCalls(impressionId, dvObj);
            }, timeoutMs);
        }
    };

    this.createEventCallUrl = function(impId, eventObject) {
        var tag = this.tags && this.tags[impId];
        if (tag && typeof eventObject !== 'undefined' && eventObject !== null) {
            return ['https://', tag.ServerPublicDns, '/bsevent.gif?impid=', impId, '&', createQueryStringParams(eventObject)].join('');
        }
    }

    var dispatchEventCallsNow = function (dvObj, impressionId, eventObject) {
        addEventCallForDispatch(impressionId, eventObject);
        dispatchEventCalls(impressionId, dvObj);
    };

    var addEventCallForDispatch = function (impressionId, eventObject) {
        for (var key in eventObject) {
            if (typeof eventObject[key] !== 'function' && eventObject.hasOwnProperty(key)) {
                if (!eventsForDispatch[impressionId])
                    eventsForDispatch[impressionId] = {};
                eventsForDispatch[impressionId][key] = eventObject[key];
            }
        }
    };

    if (window.addEventListener) {
        window.addEventListener('unload', function () {
            that.dispatchRegisteredEventsFromAllTags();
        }, false);
        window.addEventListener('beforeunload', function () {
            that.dispatchRegisteredEventsFromAllTags();
        }, false);
    }
    else if (window.attachEvent) {
        window.attachEvent('onunload', function () {
            that.dispatchRegisteredEventsFromAllTags();
        }, false);
        window.attachEvent('onbeforeunload', function () {
            that.dispatchRegisteredEventsFromAllTags();
        }, false);
    }
    else {
        window.document.body.onunload = function () {
            that.dispatchRegisteredEventsFromAllTags();
        };
        window.document.body.onbeforeunload = function () {
            that.dispatchRegisteredEventsFromAllTags();
        };
    }

    var createQueryStringParams = function (values) {
        var params = '';
        for (var key in values) {
            if (typeof values[key] !== 'function') {
                var value = encodeURIComponent(values[key]);
                if (params === '')
                    params += key + '=' + value;
                else
                    params += '&' + key + '=' + value;
            }
        }

        return params;
    };
}

function dv_baseHandler(){function K(b){var d=window._dv_win,e=0;try{for(;10>e;){if(d[b]&&"object"===typeof d[b])return!0;if(d==d.parent)break;e++;d=d.parent}}catch(c){}return!1}function E(b,d,e){e=e||150;var c=window._dv_win||window;if(c.document&&c.document.body)return d&&d.parentNode?d.parentNode.insertBefore(b,d):c.document.body.insertBefore(b,c.document.body.firstChild),!0;if(0<e)setTimeout(function(){E(b,d,--e)},20);else return!1}function L(b){var d=window._dv_win.dv_config=window._dv_win.dv_config||
{};d.cdnAddress=d.cdnAddress||"cdn.doubleverify.com";return'<html><head><script type="text/javascript">('+function(){try{window.$dv=window.$dvbs||parent.$dvbs,window.$dv.dvObjType="dvbs"}catch(e){}}.toString()+')();\x3c/script></head><body><script type="text/javascript">('+(b||"function() {}")+')("'+d.cdnAddress+'");\x3c/script><script type="text/javascript">setTimeout(function() {document.close();}, 0);\x3c/script></body></html>'}function F(b){var d=0,e;for(e in b)b.hasOwnProperty(e)&&++d;return d}
function M(b,d){a:{var e={};try{if(b&&b.performance&&b.performance.getEntries){var c=b.performance.getEntries();for(b=0;b<c.length;b++){var f=c[b],p=f.name.match(/.*\/(.+?)\./);if(p&&p[1]){var g=p[1].replace(/\d+$/,""),h=d[g];if(h){for(var k=0;k<h.stats.length;k++){var r=h.stats[k];e[h.prefix+r.prefix]=Math.round(f[r.name])}delete d[g];if(!F(d))break}}}}var m=e;break a}catch(z){}m=void 0}if(m&&F(m))return m}function N(b){var d,e=window._dv_win.document.visibilityState;window[b.tagObjectCallbackName]=
function(c){var f=window._dv_win.$dvbs;f&&(d=c.ImpressionID,f.tags.add(c.ImpressionID,b),f.tags[c.ImpressionID].set({tagElement:b.script,impressionId:c.ImpressionID,dv_protocol:b.protocol,protocol:"https:",uid:b.uid,serverPublicDns:c.ServerPublicDns,ServerPublicDns:c.ServerPublicDns}),b.script&&b.script.dvFrmWin&&(b.script.dvFrmWin.$uid=c.ImpressionID,f.messages&&f.messages.startSendingEvents&&f.messages.startSendingEvents(b.script.dvFrmWin,c.ImpressionID)),function(){function b(){var d=window._dv_win.document.visibilityState;
"prerender"===e&&"prerender"!==d&&"unloaded"!==d&&(e=d,window._dv_win.$dvbs.registerEventCall(c.ImpressionID,{prndr:0}),window._dv_win.document.removeEventListener(f,b))}if("prerender"===e)if("prerender"!==window._dv_win.document.visibilityState&&"unloaded"!==visibilityStateLocal)window._dv_win.$dvbs.registerEventCall(c.ImpressionID,{prndr:0});else{var f;"undefined"!==typeof window._dv_win.document.hidden?f="visibilitychange":"undefined"!==typeof window._dv_win.document.mozHidden?f="mozvisibilitychange":
"undefined"!==typeof window._dv_win.document.msHidden?f="msvisibilitychange":"undefined"!==typeof window._dv_win.document.webkitHidden&&(f="webkitvisibilitychange");window._dv_win.document.addEventListener(f,b,!1)}}());if("1"!=b.foie)try{var p=M(window,{verify:{prefix:"vf",stats:[{name:"duration",prefix:"dur"}]}});p&&window._dv_win.$dvbs.registerEventCall(c.ImpressionID,p)}catch(g){}};window[b.callbackName]=function(c){u.setIsJSONPCalled(!0);var f=window._dv_win.$dvbs&&"object"==typeof window._dv_win.$dvbs.tags[d]?
window._dv_win.$dvbs.tags[d]:b;var e=window._dv_win.dv_config.bs_renderingMethod||function(b){document.write(b)};switch(c.ResultID){case 1:f.tagPassback?e(f.tagPassback):c.Passback?e(decodeURIComponent(c.Passback)):c.AdWidth&&c.AdHeight&&e(decodeURIComponent("%3Cdiv%20style%3D%22display%3A%20flex%3B%20align-items%3A%20center%3B%20justify-content%3A%20center%3B%20width%3A%20"+c.AdWidth+"px%3B%20height%3A%20"+c.AdHeight+"px%3B%20outline-offset%3A%20-1px%3B%20background%3A%20url('data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAADoAAAA6CAYAAAGWvHq%2BAAAABmJLR0QA%2FwD%2FAP%2BgvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5AQBECEbFuFN7gAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAAFBklEQVRo3uUby3arOEzxAbxIyKLt%2F%2F9gIQtIF4aFZ5ERVxhJyIbcnjmjTZLast4vQ%2BG762OMMX53fQzTFIfxGenfKvgXvj4%2FoOsfy3eECgBgmmcYhnFZ6PoHeO%2F%2FbBiGEQAAxufPghlC%2BLOBYqa%2FHezAJcYYOUz87QAA7vd2g4lMAsrLfQJ%2BQeUM43PZsMJEwN8L58gMfgIAAMVKv6syX4bxGVF9qTiuvV2Byouf7e0Kl%2B%2Buj6kJU8aktV07aFClTkThfm9hGMbNGu53dCNd%2FPr8gBCm5TsnAivz%2BPwBqkHvPaDiVvpAW6Nh0FBhmpagSdfQV0Q7oVySPrz3LyO3t%2BvCKrJIHTtdG58%2FvLycZk%2Bzr1uFkgFWuYHKZHHNEMIr4lMb0pO5v7e3qyyj983KATYydv1jswFZneZ5wzaKVaEMVnNgjsw2B8pcbMdLmKbY1PVG5dTl0rVpnsGlSDReOcfo%2Bgc0df3SagrTPC8m4aDrH1ClaR4AgHKRmgN%2FL9HBbeI4wdKVitXUtYpLGXPSgpUg1lBaPzWCWW6wJ4lkB9aFUL1pQkXOvW9WBDltULNM8wwhTEtIcQn88t31kdpEU7FmOwsemqiiqtPsQvufXMCmCulUSKy9XaG9XYGrLhbv1iSlWU0NGdyQqlPKBHQfh0vxVkQ1abSQybX3oQ7nUPWUpEQ1oaokLVAnSfG4cy8xxpjrEFyVtuCJNt3rETDgu%2F6xiT9zRqKSci0DxzHdZ5E0zXabjGTtwSxr9FyqjazSJkmTi%2Bckb01BS5HaGnems%2BZWzdb62qQTfQdwDDl2Wj0RuKnYpX1sDrJljcvHTqow4%2FNn5SBNXYuzPD0Y8agDsRlpr3NIg1vyYGnSS%2BPUURVIcRhC2A0ZyYPxTKqNyuo8IYRlpMSGLYRJDRdOYyEEqEpDIIfY5qYhhLBrL0s%2BLS7imqq995tijYVdCxlx0EMnaW9XlvD93m4aZ0s4cZ3gqspYOjppRKcMcXipGZyU7Ju63iXIhVOKx53trCWqtMpwZzor8n%2BqynBnnlJlNGa5M51VSmlksBSDlOHlKk%2FzUq0KcVVEYgidytz3coS19lPrFh1y2fUP1Xu1HKsRxHWakao9hLNglZHeESaal3vvocKx3zKP7BXnLJtaxgNkjKY1Wp1y7inYUVG7Akg79vSeKefKwHJ1kEtTikBxJrYkmpIBr1TgPdgbrZ1WkPbuz84UEiNZG1ZLhdydE0sqeqlytGG2pEt4%2B0Ccc9H8zs4kS1Br0542F0fqR0lesOCwyehoIioZq86gqcWq6XbZwrTGqMSAhmOhKWVpjp74PObIsLt3R3g0g1oETs8R32woFbLEHUuEs9CiZa6SslZJmpcuf%2F4GcNc0tDf9lYcxvwGVrI3mkDVeY0NjbumOui9XCtkYlZJIbjt3pF8tzQ0czZTvTXnJSdlHSstRXAlPUpQ4vRy1TK4nnNEwaDTd2ZNE6fQSQiieevBiprjXLamjpco5Mv1YSuH%2Fpry4o%2BMPN70cgZI4tYyG7h3J4evzI1tJ%2BIynBLTHMdnlpXQKsTQCkoAaPakZEctL%2BpbK0Y7FMkloCnrXHMsKileMpS0ZR3zvveez2kDJG6szRiSuJqaulfbOaQJ5KfcYH5wnLK82v2uMCmHaPDz%2BDVj%2BfSNNBGdZmIu9v6EIKWbVZHTmVYrl9clSRVsS0urOKDdlW1J%2B6SubFoH3SiF13X8A3uobUgsAG3MAAAAASUVORK5CYII%3D')%20repeat%3B%20outline%3A%20solid%201px%20%23969696%3B%22%3E%3C%2Fdiv%3E"));
break;case 2:case 3:f.tagAdtag&&e(f.tagAdtag);break;case 4:c.AdWidth&&c.AdHeight&&e(decodeURIComponent("%3Cstyle%3E%0A.dvbs_container%20%7B%0A%09border%3A%201px%20solid%20%233b599e%3B%0A%09overflow%3A%20hidden%3B%0A%09filter%3A%20progid%3ADXImageTransform.Microsoft.gradient(startColorstr%3D%27%23315d8c%27%2C%20endColorstr%3D%27%2384aace%27)%3B%0A%7D%0A%3C%2Fstyle%3E%0A%3Cdiv%20class%3D%22dvbs_container%22%20style%3D%22width%3A%20"+c.AdWidth+"px%3B%20height%3A%20"+c.AdHeight+"px%3B%22%3E%09%0A%3C%2Fdiv%3E"))}}}
function O(b){var d=null,e=null,c=function(b){var c=dv_GetParam(b,"cmp");b=dv_GetParam(b,"ctx");return"919838"==b&&"7951767"==c||"919839"==b&&"7939985"==c||"971108"==b&&"7900229"==c||"971108"==b&&"7951940"==c?"</scr'+'ipt>":/<\/scr\+ipt>/g}(b.src);"function"!==typeof String.prototype.trim&&(String.prototype.trim=function(){return this.replace(/^\s+|\s+$/g,"")});var f=function(b){!(b=b.previousSibling)||"#text"!=b.nodeName||null!=b.nodeValue&&void 0!=b.nodeValue&&0!=b.nodeValue.trim().length||(b=b.previousSibling);
if(b&&"SCRIPT"==b.tagName&&b.getAttribute("type")&&("text/adtag"==b.getAttribute("type").toLowerCase()||"text/passback"==b.getAttribute("type").toLowerCase())&&""!=b.innerHTML.trim()){if("text/adtag"==b.getAttribute("type").toLowerCase())return d=b.innerHTML.replace(c,"\x3c/script>"),{isBadImp:!1,hasPassback:!1,tagAdTag:d,tagPassback:e};if(null!=e)return{isBadImp:!0,hasPassback:!1,tagAdTag:d,tagPassback:e};e=b.innerHTML.replace(c,"\x3c/script>");b=f(b);b.hasPassback=!0;return b}return{isBadImp:!0,
hasPassback:!1,tagAdTag:d,tagPassback:e}};return f(b)}function G(b,d,e,c,f,p,g,h,k,r,m,z){d.dvregion=0;var v=dv_GetParam(l,"useragent");l=window._dv_win.$dvbs.CommonData;if(void 0!=l.BrowserId&&void 0!=l.BrowserVersion&&void 0!=l.BrowserIdFromUserAgent)var n={ID:l.BrowserId,version:l.BrowserVersion,ID_UA:l.BrowserIdFromUserAgent};else n=P(v?decodeURIComponent(v):navigator.userAgent),l.BrowserId=n.ID,l.BrowserVersion=n.version,l.BrowserIdFromUserAgent=n.ID_UA;var q="";void 0!=d.aUrl&&(q="&aUrl="+d.aUrl);
var A="";try{c.depth=Q(c);var w=R(c,e,n);if(w&&w.duration){var u="&dvp_strhd="+w.duration;u+="&dvpx_strhd="+w.duration}w&&w.url||(w=S(c));w&&w.url&&(q="&aUrl="+encodeURIComponent(w.url),A="&aUrlD="+w.depth);var x=c.depth+f;p&&c.depth--}catch(H){u=A=q=x=c.depth=""}a:{try{if("object"==typeof window.$ovv||"object"==typeof window.parent.$ovv){var t=1;break a}}catch(H){}t=0}f=function(){function b(c){f++;var d=c.parent==c;return c.mraid||d?c.mraid:20>=f&&b(c.parent)}var c=window._dv_win||window,f=0;try{return b(c)}catch(ca){}}();
var l=d.script.src;t="&ctx="+(dv_GetParam(l,"ctx")||"")+"&cmp="+(dv_GetParam(l,"cmp")||"")+"&plc="+(dv_GetParam(l,"plc")||"")+"&sid="+(dv_GetParam(l,"sid")||"")+"&advid="+(dv_GetParam(l,"advid")||"")+"&adsrv="+(dv_GetParam(l,"adsrv")||"")+"&unit="+(dv_GetParam(l,"unit")||"")+"&isdvvid="+(dv_GetParam(l,"isdvvid")||"")+"&uid="+d.uid+"&tagtype="+(dv_GetParam(l,"tagtype")||"")+"&adID="+(dv_GetParam(l,"adID")||"")+"&app="+(dv_GetParam(l,"app")||"")+"&sup="+(dv_GetParam(l,"sup")||"")+"&isovv="+t+"&gmnpo="+
(dv_GetParam(l,"gmnpo")||"")+"&crt="+(dv_GetParam(l,"crt")||"");"1"==dv_GetParam(l,"foie")&&(t+="&foie=1");f&&(t+="&ismraid=1");(f=dv_GetParam(l,"xff"))&&(t+="&xff="+f);(f=dv_GetParam(l,"vssd"))&&(t+="&vssd="+f);(f=dv_GetParam(l,"apifw"))&&(t+="&apifw="+f);(f=dv_GetParam(l,"vstvr"))&&(t+="&vstvr="+f);(f=dv_GetParam(l,"tvcp"))&&(t+="&tvcp="+f);m&&(t+="&urlsrc=sf");z&&(t+="&sfe=1");navigator&&navigator.maxTouchPoints&&5==navigator.maxTouchPoints&&(t+="&touch=1");u&&(t+=u);v&&(t+="&useragent="+v);n&&
(t+="&brid="+n.ID+"&brver="+n.version+"&bridua="+n.ID_UA);t+="&dup="+dv_GetParam(l,"dup");try{t+=dv_AppendIQPAParams(l)}catch(H){}(m=dv_GetParam(l,"turl"))&&(t+="&turl="+m);(m=dv_GetParam(l,"tagformat"))&&(t+="&tagformat="+m);t+=U();r=r?"&dvf=0":"";m=K("maple")?"&dvf=1":"";c=(window._dv_win.dv_config.verifyJSURL||"https://"+(window._dv_win.dv_config.bsAddress||"rtb"+d.dvregion+".doubleverify.com")+"/verify.js")+"?jsCallback="+d.callbackName+"&jsTagObjCallback="+d.tagObjectCallbackName+"&num=6"+t+
"&srcurlD="+c.depth+"&ssl="+d.ssl+r+m+"&refD="+x+d.tagIntegrityFlag+d.tagHasPassbackFlag+"&htmlmsging="+(g?"1":"0");(g=dv_GetDynamicParams(l,"dvp").join("&"))&&(c+="&"+g);(g=dv_GetDynamicParams(l,"dvpx").join("&"))&&(c+="&"+g);if(!1===h||k)c=c+("&dvp_isBodyExistOnLoad="+(h?"1":"0"))+("&dvp_isOnHead="+(k?"1":"0"));e="srcurl="+encodeURIComponent(e);(h=V())&&(e+="&ancChain="+encodeURIComponent(h));h=4E3;/MSIE (\d+\.\d+);/.test(navigator.userAgent)&&7>=new Number(RegExp.$1)&&(h=2E3);if(k=dv_GetParam(l,
"referrer"))k="&referrer="+k,c.length+k.length<=h&&(c+=k);(k=dv_GetParam(l,"prr"))&&(c+="&prr="+k);(k=dv_GetParam(l,"iframe"))&&(c+="&iframe="+k);(k=dv_GetParam(l,"gdpr"))&&(c+="&gdpr="+k);(k=dv_GetParam(l,"gdpr_consent"))&&(c+="&gdpr_consent="+k);q.length+A.length+c.length<=h&&(c+=A,e+=q);(q=W())&&(c+="&m1="+q);(q=X())&&0<q.f&&(c+="&bsig="+q.f,c+="&usig="+q.s);q=Y();0<q&&(c+="&hdsig="+q);navigator&&navigator.hardwareConcurrency&&(c+="&noc="+navigator.hardwareConcurrency);c+=Z();q=aa();c+="&vavbkt="+
q.vdcd;c+="&lvvn="+q.vdcv;""!=q.err&&(c+="&dvp_idcerr="+encodeURIComponent(q.err));"prerender"===window._dv_win.document.visibilityState&&(c+="&prndr=1");(l=dv_GetParam(l,"wrapperurl"))&&1E3>=l.length&&c.length+l.length<=h&&(c+="&wrapperurl="+l);c+="&"+b.getVersionParamName()+"="+b.getVersion();b="&eparams="+encodeURIComponent(C(e));c=c.length+b.length<=h?c+b:c+"&dvf=3";window.performance&&window.performance.mark&&window.performance.measure&&window.performance.getEntriesByName&&(window.performance.mark("dv_create_req_end"),
window.performance.measure("dv_creqte_req","dv_create_req_start","dv_create_req_end"),(b=window.performance.getEntriesByName("dv_creqte_req"))&&0<b.length&&(c+="&dvp_exetime="+b[0].duration.toFixed(2)));for(var y in d)d.hasOwnProperty(y)&&void 0!==d[y]&&-1<["number","string"].indexOf(typeof d[y])&&-1===["protocol","callbackName","dvregion"].indexOf(y.toLowerCase())&&!y.match(/^tag[A-Z]/)&&!(new RegExp("(\\?|&)"+y+"=","gi")).test(c)&&(c+=["&",y,"=",encodeURIComponent(d[y])].join(""));return{isSev1:!1,
url:c}}function U(){var b="";try{var d=window._dv_win.parent;b+="&chro="+(void 0===d.chrome?"0":"1");b+="&hist="+(d.history?d.history.length:"");b+="&winh="+d.innerHeight;b+="&winw="+d.innerWidth;b+="&wouh="+d.outerHeight;b+="&wouw="+d.outerWidth;d.screen&&(b+="&scah="+d.screen.availHeight,b+="&scaw="+d.screen.availWidth)}catch(e){}return b}function aa(){var b=[],d=function(b){c(b,null!=b.AZSD,9);c(b,b.location.hostname!=b.encodeURIComponent(b.location.hostname),10);c(b,null!=b.cascadeWindowInfo,
11);c(b,null!=b._rvz,32);c(b,null!=b.FO_DOMAIN,34);c(b,null!=b.va_subid,36);c(b,b._GPL&&b._GPL.baseCDN,40);c(b,e(b,"__twb__")&&e(b,"__twb_cb_"),43);c(b,null!=b.landingUrl&&null!=b.seList&&null!=b.parkingPPCTitleElements&&null!=b.allocation,45);c(b,e(b,"_rvz",function(b){return null!=b.publisher_subid}),46);c(b,null!=b.cacildsFunc&&null!=b.n_storesFromFs,47);c(b,b._pcg&&b._pcg.GN_UniqueId,54);c(b,e(b,"__ad_rns_")&&e(b,"_$_"),64);c(b,null!=b.APP_LABEL_NAME_FULL_UC,71);c(b,null!=b._priam_adblock,81);
c(b,b.supp_ads_host&&b.supp_ads_host_overridden,82);c(b,b.uti_xdmsg_manager&&b.uti_xdmsg_manager.cb,87);c(b,b.LogBundleData&&b.addIframe,91);c(b,b.xAdsXMLHelperId||b.xYKAffSubIdTag,95);c(b,b.__pmetag&&b.__pmetag.uid,98);c(b,b.CustomWLAdServer&&/(n\d{1,4}adserv)|(1ads|cccpmo|epommarket|epmads|adshost1)/.test(b.supp_ads_host_overridden),100)},e=function(b,c,d){for(var e in b)if(-1<e.indexOf(c)&&(!d||d(b[e])))return!0;return!1},c=function(c,d,e){d&&-1==b.indexOf(e)&&b.push((c==window.top?-1:1)*e)};try{return function(){for(var b=
window,c=0;10>c&&(d(b),b!=window.top);c++)try{b.parent.document&&(b=b.parent)}catch(g){break}}(),{vdcv:28,vdcd:b.join(","),err:void 0}}catch(f){return{vdcv:28,vdcd:"-999",err:f.message||"unknown"}}}function Q(b){for(var d=0;10>d&&b!=window._dv_win.top;)d++,b=b.parent;return d}function R(b,d,e){try{var c;if(!(c=e.ID==$dvbs.Enums.BrowserId.IE)){if(b==window._dv_win.top)var f=$dvbs.Enums.TrafficScenario.OnPage;else{e=b;try{for(var p=0;window._dv_win.top!=e&&10>=p;){var g=e.parent;if(!g.document)break;
e=g;p++}}catch(T){}f=e==window._dv_win.top?$dvbs.Enums.TrafficScenario.SameDomain:$dvbs.Enums.TrafficScenario.CrossDomain}c=f!=$dvbs.Enums.TrafficScenario.CrossDomain}if(c)return null;b.performance&&b.performance.mark&&b.performance.mark("dv_str_html_start");if(d){var h=d.toString().match(/^(?:https?:\/\/)?[\w\-\.]+\/[a-zA-Z0-9]/gi);if(h&&0<h.length)return null}var k=b.document;if(k&&k.referrer){var r=k.referrer.replace(/\//g,"\\/").replace(/\./g,"\\."),m=new RegExp('(?:w{0,4}=")?'+r+"[^&\"; %,'\\$\\\\\\|]+",
"gi");d=/banner|adprefs|safeframe|sandbox|sf\.html/gi;c=/^\w{0,4}="/gi;var z=I(k,"script","src",m,d,c);if(!z){var v=k.referrer;f="";var n=k.getElementsByTagName("script");if(n)for(g=0;!f&&g<n.length;){var q=n[g].innerHTML;if(q&&-1!=q.indexOf(v)){var A=q.match(m);f=J(A,d,c)}g++}(z=f)||(z=I(k,"a","href",m,d,c))}k=htmlUrl=z;a:{if(b.performance&&b.performance.mark&&b.performance.measure&&b.performance.getEntriesByName){b.performance.mark("dv_str_html_end");b.performance.measure("dv_str_html","dv_str_html_start",
"dv_str_html_end");var w=b.performance.getEntriesByName("dv_str_html");if(w&&0<w.length){var u=w[0].duration.toFixed(2);break a}}u=null}return{url:k,depth:-1,duration:u}}}catch(T){}return null}function J(b,d,e){var c="";if(b&&0<b.length)for(var f=0;f<b.length;f++){var p=b[f];p.length>c.length&&null==p.match(d)&&0!=p.indexOf('src="')&&0!=p.indexOf('turl="')&&(c=p.replace(e,""))}return c}function I(b,d,e,c,f,p){b=b.querySelectorAll(d+"["+e+'*="'+b.referrer+'"]');var g="";if(b)for(d=0;!g&&d<b.length;)g=
b[d][e].match(c),g=J(g,f,p),d++;return g}function S(b){try{if(1>=b.depth)return{url:"",depth:""};var d=[];d.push({win:window._dv_win.top,depth:0});for(var e,c=1,f=0;0<c&&100>f;){try{if(f++,e=d.shift(),c--,0<e.win.location.toString().length&&e.win!=b)return 0==e.win.document.referrer.length||0==e.depth?{url:e.win.location,depth:e.depth}:{url:e.win.document.referrer,depth:e.depth-1}}catch(h){}var p=e.win.frames.length;for(var g=0;g<p;g++)d.push({win:e.win.frames[g],depth:e.depth+1}),c++}return{url:"",
depth:""}}catch(h){return{url:"",depth:""}}}function V(){var b=window._dv_win[C("=@42E:@?")][C("2?46DE@C~C:8:?D")];if(b&&0<b.length){var d=[];d[0]=window._dv_win.location.protocol+"//"+window._dv_win.location.hostname;for(var e=0;e<b.length;e++)d[e+1]=b[e];return d.reverse().join(",")}return null}function C(b){new String;var d=new String,e;for(e=0;e<b.length;e++){var c=b.charAt(e);var f="!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~".indexOf(c);0<=
f&&(c="!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~".charAt((f+47)%94));d+=c}return d}function B(){return Math.floor(1E12*(Math.random()+""))}function P(b){for(var d=[{id:4,brRegex:"OPR|Opera",verRegex:"(OPR/|Version/)"},{id:1,brRegex:"MSIE|Trident/7.*rv:11|rv:11.*Trident/7|Edge/|Edg/",verRegex:"(MSIE |rv:| Edge/|Edg/)"},{id:2,brRegex:"Firefox",verRegex:"Firefox/"},{id:0,brRegex:"Mozilla.*Android.*AppleWebKit(?!.*Chrome.*)|Linux.*Android.*AppleWebKit.* Version/.*Chrome",
verRegex:null},{id:0,brRegex:"AOL/.*AOLBuild/|AOLBuild/.*AOL/|Puffin|Maxthon|Valve|Silk|PLAYSTATION|PlayStation|Nintendo|wOSBrowser",verRegex:null},{id:3,brRegex:"Chrome",verRegex:"Chrome/"},{id:5,brRegex:"Safari|(OS |OS X )[0-9].*AppleWebKit",verRegex:"Version/"}],e=0,c="",f=0;f<d.length;f++)if(null!=b.match(new RegExp(d[f].brRegex))){e=d[f].id;if(null==d[f].verRegex)break;b=b.match(new RegExp(d[f].verRegex+"[0-9]*"));null!=b&&(c=b[0].match(new RegExp(d[f].verRegex)),c=b[0].replace(c[0],""));break}d=
ba();4==e&&(d=e);return{ID:d,version:d===e?c:"",ID_UA:e}}function ba(){try{if(null!=window._phantom||null!=window.callPhantom)return 99;if(document.documentElement.hasAttribute&&document.documentElement.hasAttribute("webdriver")||null!=window.domAutomation||null!=window.domAutomationController||null!=window._WEBDRIVER_ELEM_CACHE)return 98;if(void 0!=window.opera&&void 0!=window.history.navigationMode||void 0!=window.opr&&void 0!=window.opr.addons&&"function"==typeof window.opr.addons.installExtension)return 4;
if(void 0!=document.uniqueID&&"string"==typeof document.uniqueID&&(void 0!=document.documentMode&&0<=document.documentMode||void 0!=document.all&&"object"==typeof document.all||void 0!=window.ActiveXObject&&"function"==typeof window.ActiveXObject)||window.document&&window.document.updateSettings&&"function"==typeof window.document.updateSettings||Object.values&&navigator&&Object.values(navigator.plugins).some(function(b){return-1!=b.name.indexOf("Edge PDF")}))return 1;if(void 0!=window.chrome&&"function"==
typeof window.chrome.csi&&"function"==typeof window.chrome.loadTimes&&void 0!=document.webkitHidden&&(1==document.webkitHidden||0==document.webkitHidden))return 3;if(void 0!=window.mozInnerScreenY&&"number"==typeof window.mozInnerScreenY&&void 0!=window.mozPaintCount&&0<=window.mozPaintCount&&void 0!=window.InstallTrigger&&void 0!=window.InstallTrigger.install)return 2;var b=!1;try{var d=document.createElement("p");d.innerText=".";d.style="text-shadow: rgb(99, 116, 171) 20px -12px 2px";b=void 0!=
d.style.textShadow}catch(e){}return(0<Object.prototype.toString.call(window.HTMLElement).indexOf("Constructor")||window.webkitAudioPannerNode&&window.webkitConvertPointFromNodeToPage)&&b&&void 0!=window.innerWidth&&void 0!=window.innerHeight?5:0}catch(e){return 0}}function W(){try{var b=0,d=function(c,d){d&&32>c&&(b=(b|1<<c)>>>0)},e=function(b,c){return function(){return b.apply(c,arguments)}},c="svg"===document.documentElement.nodeName.toLowerCase(),f=function(){return"function"!==typeof document.createElement?
document.createElement(arguments[0]):c?document.createElementNS.call(document,"http://www.w3.org/2000/svg",arguments[0]):document.createElement.apply(document,arguments)},p=["Moz","O","ms","Webkit"],g=["moz","o","ms","webkit"],h={style:f("modernizr").style},k=function(b,c){function d(){m&&(delete h.style,delete h.modElem)}var e;for(e=["modernizr","tspan","samp"];!h.style&&e.length;){var m=!0;h.modElem=f(e.shift());h.style=h.modElem.style}var g=b.length;for(e=0;e<g;e++){var k=b[e];~(""+k).indexOf("-")&&
(k=cssToDOM(k));if(void 0!==h.style[k])return d(),"pfx"==c?k:!0}d();return!1},r=function(b,c,d){var f=b.charAt(0).toUpperCase()+b.slice(1),h=(b+" "+p.join(f+" ")+f).split(" ");if("string"===typeof c||"undefined"===typeof c)return k(h,c);h=(b+" "+g.join(f+" ")+f).split(" ");for(var m in h)if(h[m]in c){if(!1===d)return h[m];b=c[h[m]];return"function"===typeof b?e(b,d||c):b}return!1};d(0,!0);d(1,r("requestFileSystem",window));d(2,window.CSS?"function"==typeof window.CSS.escape:!1);d(3,r("shapeOutside",
"content-box",!0));return b}catch(m){return 0}}function D(){var b=window,d=0;try{for(;b.parent&&b!=b.parent&&b.parent.document&&!(b=b.parent,10<d++););}catch(e){}return b}function X(){try{var b=D(),d=0,e=0,c=function(b,c,f){f&&(d+=Math.pow(2,b),e+=Math.pow(2,c))},f=b.document;c(14,0,b.playerInstance&&f.querySelector('script[src*="ads-player.com"]'));c(14,1,(b.CustomWLAdServer||b.DbcbdConfig)&&(a=f.querySelector('p[class="footerCopyright"]'),a&&a.textContent.match(/ MangaLife 2016/)));c(15,2,b.zpz&&
b.zpz.createPlayer);c(15,3,b.vdApp&&b.vdApp.createPlayer);c(15,4,f.querySelector('body>div[class="z-z-z"]'));c(16,5,b.xy_checksum&&b.place_player&&(b.logjwonready&&b.logContentPauseRequested||b.jwplayer));c(17,6,b==b.top&&""==f.title?(a=f.querySelector('body>object[id="player"]'),a&&a.data&&1<a.data.indexOf("jwplayer")&&"visibility: visible;"==a.getAttribute("style")):!1);c(17,7,f.querySelector('script[src*="sitewebvideo.com"]'));c(17,8,b.InitPage&&b.cef&&b.InitAd);c(17,9,b==b.top&&""==f.title?(a=
f.querySelector("body>#player"),null!=a&&null!=(null!=a.querySelector('div[id*="opti-ad"]')||a.querySelector('iframe[src="about:blank"]'))):!1);c(17,10,b==b.top&&""==f.title&&b.InitAdPlayer?(a=f.querySelector('body>div[id="kt_player"]'),null!=a&&null!=a.querySelector('div[class="flash-blocker"]')):!1);c(17,11,null!=b.clickplayer&&null!=b.checkRdy2);c(19,12,b.instance&&b.inject&&f.querySelector('path[id="cp-search-0"]'));c(20,13,function(){try{if(b.top==b&&0<b.document.getElementsByClassName("asu").length)for(var c=
b.document.styleSheets,d=0;d<c.length;d++)for(var e=b.document.styleSheets[d].cssRules,f=0;f<e.length;f++)if("div.kk"==e[f].selectorText||"div.asu"==e[f].selectorText)return!0}catch(q){}}());a:{try{var p=null!=f.querySelector('div[id="kt_player"][hiegth]');break a}catch(m){}p=void 0}c(21,14,p);a:{try{var g=b.top==b&&null!=b.document.querySelector('div[id="asu"][class="kk"]');break a}catch(m){}g=void 0}c(22,15,g);a:{try{var h=f.querySelector('object[data*="/VPAIDFlash.swf"]')&&f.querySelector('object[id*="vpaid_video_flash_tester_el"]')&&
f.querySelector('div[id*="desktopSubModal"]');break a}catch(m){}h=void 0}c(25,16,h);var k=navigator.userAgent;if(k&&-1<k.indexOf("Android")&&-1<k.indexOf(" wv)")&&b==window.top){var r=f.querySelector('img[src*="dealsneartome.com"]')||(b.__cads__?!0:!1)||0<f.querySelectorAll('img[src*="/tracker?tag="]').length;c(28,17,r||!1)}return{f:d,s:e}}catch(m){return null}}function Y(){try{var b=D(),d=0,e=b.document;b==window.top&&""==e.title&&!e.querySelector("meta[charset]")&&e.querySelector('div[style*="background-image: url("]')&&
(e.querySelector('script[src*="j.pubcdn.net"]')||e.querySelector('span[class="ad-close"]'))&&(d+=Math.pow(2,6));return d}catch(c){return null}}function Z(){try{var b="&fcifrms="+window.top.length;window.history&&(b+="&brh="+window.history.length);var d=D(),e=d.document;if(d==window.top){b+="&fwc="+((d.FB?1:0)+(d.twttr?2:0)+(d.outbrain?4:0)+(d._taboola?8:0));try{e.cookie&&(b+="&fcl="+e.cookie.length)}catch(c){}d.performance&&d.performance.timing&&0<d.performance.timing.domainLookupStart&&0<d.performance.timing.domainLookupEnd&&
(b+="&flt="+(d.performance.timing.domainLookupEnd-d.performance.timing.domainLookupStart));e.querySelectorAll&&(b+="&fec="+e.querySelectorAll("*").length)}return b}catch(c){return""}}var x=this,u=function(){function b(b,d){var e=[];d&&p.forEach(function(b){var c=dv_GetParam(d,b);""!==c&&null!==c&&e.push(["dvp_"+b,c].join("="))});var g=window&&window._dv_win||{};g=g.dv_config=g.dv_config||{};g=dv_getDVBSErrAddress(g);var k=[f,c].join("="),m=["dvp_cert",h[b]].join("=");b=["dvp_jsErrMsg",b].join("=");
g+=["/verify.js?ctx=818052&cmp=1619415&dvp_isLostImp=1&ssl=1",k,m,b,e.join("&")].join("&");(new Image(1,1)).src="https://"+g}function d(c,d){var e=window._dv_win.dv_config.bs_renderingMethod||function(b){document.write(b)};d="AdRenderedUponVerifyFailure__"+(d||"");if(x&&x.tagParamsObj&&x.tagParamsObj.tagAdtag)try{e(x.tagParamsObj.tagAdtag)}catch(v){d+="__RenderingMethodFailed"}else x?x.tagParamsObj?x.tagParamsObj.tagAdtag||(d+="__HandlerTagParamsObjTagAdtag__Undefined"):d+="__HandlerTagParamsObj__Undefined":
d+="__Handler__Undefined";b(d,c)}var e=!1,c,f,p=["ctx","cmp","plc","sid"],g=[x.constructor&&x.constructor.name||"UKDV","__",B()].join(""),h={VerifyLoadJSONPCallbackFailed:1,VerifyFailedToLoad:2},k={onResponse:function(c){e||(b("VerifyCallbackFailed",c),d(c,"VCF"))},onError:function(c){b("VerifyFailedToLoad",c);d(c,"VFTL")}};k.reportError=b;k.isJSONPCalled=e;window._dv_win[g]={globalScopeVerifyErrorHandler:k};return{setVersionData:function(b,d){f=b;c=d},setIsJSONPCalled:function(b){e=b},getIsJSONPCalled:function(){return e},
onLoad:dv_onResponse,onError:dv_onError,uniqueKey:g}}();this.createRequest=function(){window.performance&&window.performance.mark&&window.performance.mark("dv_create_req_start");var b=!1,d=window._dv_win,e=0,c=!1,f;try{for(f=0;10>=f;f++)if(null!=d.parent&&d.parent!=d)if(0<d.parent.location.toString().length)d=d.parent,e++,b=!0;else{b=!1;break}else{0==f&&(b=!0);break}}catch(q){b=!1}a:{try{var p=d.$sf;break a}catch(q){}p=void 0}var g=(f=d.location&&d.location.ancestorOrigins)&&f[f.length-1];if(0==d.document.referrer.length)b=
d.location;else if(b)b=d.location;else{b=d.document.referrer;a:{try{var h=d.$sf&&d.$sf.ext&&d.$sf.ext.hostURL&&d.$sf.ext.hostURL();break a}catch(q){}h=void 0}if(h&&(!f||0==h.indexOf(g))){b=h;var k=!0}c=!0}if(!window._dv_win.dvbsScriptsInternal||!window._dv_win.dvbsProcessed||0==window._dv_win.dvbsScriptsInternal.length)return{isSev1:!1,url:null};f=window._dv_win.dv_config&&window._dv_win.dv_config.isUT?window._dv_win.dvbsScriptsInternal[window._dv_win.dvbsScriptsInternal.length-1]:window._dv_win.dvbsScriptsInternal.pop();
h=f.script;this.dv_script_obj=f;this.dv_script=h;window._dv_win.dvbsProcessed.push(f);window._dv_win._dvScripts.push(h);g=h.src;this.dvOther=0;this.dvStep=1;var r=window._dv_win.dv_config?window._dv_win.dv_config.dv_GetRnd?window._dv_win.dv_config.dv_GetRnd():B():B();f=window.parent.postMessage&&window.JSON;var m={};try{for(var u=/[\?&]([^&]*)=([^&#]*)/gi,v=u.exec(g);null!=v;)"eparams"!==v[1]&&(m[v[1]]=v[2]),v=u.exec(g);var n=m}catch(q){n=m}this.tagParamsObj=n;n.perf=this.perf;n.uid=r;n.script=this.dv_script;
n.callbackName="__verify_callback_"+n.uid;n.tagObjectCallbackName="__tagObject_callback_"+n.uid;n.tagAdtag=null;n.tagPassback=null;n.tagIntegrityFlag="";n.tagHasPassbackFlag="";0==(null!=n.tagformat&&"2"==n.tagformat)&&(v=O(n.script),n.tagAdtag=v.tagAdTag,n.tagPassback=v.tagPassback,v.isBadImp?n.tagIntegrityFlag="&isbadimp=1":v.hasPassback&&(n.tagHasPassbackFlag="&tagpb=1"));v=(/iPhone|iPad|iPod|\(Apple TV|iOS|Coremedia|CFNetwork\/.*Darwin/i.test(navigator.userAgent)||navigator.vendor&&"apple, inc."===
navigator.vendor.toLowerCase())&&!window.MSStream;n.protocol="https:";n.ssl="1";g=n;(r=window._dv_win.dvRecoveryObj)?("2"!=g.tagformat&&(r=r[g.ctx]?r[g.ctx].RecoveryTagID:r._fallback_?r._fallback_.RecoveryTagID:1,1===r&&g.tagAdtag?document.write(g.tagAdtag):2===r&&g.tagPassback&&document.write(g.tagPassback)),g=!0):g=!1;if(g)return{isSev1:!0};this.dvStep=2;N(n);h=h&&h.parentElement&&h.parentElement.tagName&&"HEAD"===h.parentElement.tagName;this.dvStep=3;return G(this,n,b,d,e,c,f,!0,h,v,k,p)};this.sendRequest=
function(b){var d=dv_GetParam(b,"tagformat");if(u)try{u.setVersionData(this.getVersionParamName(),this.getVersion()),d&&"2"==d?$dvbs.domUtilities.addScriptResource(b,document.body,u.onLoad,u.onError,u.uniqueKey):dv_sendScriptRequest(b,u.onLoad,u.onError,u.uniqueKey)}catch(m){d&&"2"==d?$dvbs.domUtilities.addScriptResource(b,document.body):dv_sendScriptRequest(b)}else d&&"2"==d?$dvbs.domUtilities.addScriptResource(b,document.body):dv_sendScriptRequest(b);try{if("1"!=dv_GetParam(b,"foie")){var e=L(this.dv_script_obj&&
this.dv_script_obj.injScripts),c=document.createElement("iframe");c.name=window._dv_win.dv_config.emptyIframeID||"iframe_"+B();c.width=0;c.height=0;c.id=void 0;c.style.display="none";c.src="about:blank";c.id=c.name;var f=c.id.replace("iframe_","");c&&"function"===typeof c.setAttribute&&c.setAttribute("data-dv-frm",f);E(c,this.dv_script);if(this.dv_script){var p=this.dv_script;a:{b=null;try{if(b=c.contentWindow){var g=b;break a}}catch(m){}try{if(b=window._dv_win.frames&&window._dv_win.frames[c.name]){g=
b;break a}}catch(m){}g=null}p.dvFrmWin=g}a:{var h;if(c&&(h=c.contentDocument||c.contentWindow&&c.contentWindow.document)){var k=h;break a}k=(h=window._dv_win.frames&&window._dv_win.frames[c.name]&&window._dv_win.frames[c.name].document)?h:null}if(k)k.open(),k.write(e);else{try{document.domain=document.domain}catch(m){}var r=encodeURIComponent(e.replace(/'/g,"\\'").replace(/\n|\r\n|\r/g,""));c.src='javascript: (function(){document.open();document.domain="'+window.document.domain+"\";document.write('"+
r+"');})()"}}}catch(m){e=window._dv_win.dv_config=window._dv_win.dv_config||{},e=dv_getDVBSErrAddress(e),c=[this.getVersionParamName(),this.getVersion()].join("="),e+=["/verify.js?ctx=818052&cmp=1619415&dvp_cert=3&num=6",c].join("&"),dv_SendErrorImp(e,[{dvp_jsErrMsg:"DvFrame: "+encodeURIComponent(m)}])}return!0};this.isApplicable=function(){return!0};this.onFailure=function(){};window.debugScript&&(window.CreateUrl=G);this.getVersionParamName=function(){return"ver"};this.getVersion=function(){return"150"}}
;


function dvbs_src_main(dvbs_baseHandlerIns, dvbs_handlersDefs) {

    this.bs_baseHandlerIns = dvbs_baseHandlerIns;
    this.bs_handlersDefs = dvbs_handlersDefs;

    this.exec = function () {
        try {
            window._dv_win = (window._dv_win || window);
            window._dv_win.$dvbs = (window._dv_win.$dvbs || new dvBsType());

            window._dv_win.dv_config = window._dv_win.dv_config || {};
            window._dv_win.dv_config.bsErrAddress = window._dv_win.dv_config.bsAddress || 'rtb0.doubleverify.com';

            var errorsArr = (new dv_rolloutManager(this.bs_handlersDefs, this.bs_baseHandlerIns)).handle();
            if (errorsArr && errorsArr.length > 0)
                dv_SendErrorImp(window._dv_win.dv_config.bsErrAddress + '/verify.js?ctx=818052&cmp=1619415&num=6', errorsArr);
        }
        catch (e) {
            try {
                dv_SendErrorImp(window._dv_win.dv_config.bsErrAddress + '/verify.js?ctx=818052&cmp=1619415&num=6&dvp_isLostImp=1', {dvp_jsErrMsg: encodeURIComponent(e)});
            } catch (e) {
            }
        }
    };
};

try {
    window._dv_win = window._dv_win || window;
    var dv_baseHandlerIns = new dv_baseHandler();
	

    var dv_handlersDefs = [];
    (new dvbs_src_main(dv_baseHandlerIns, dv_handlersDefs)).exec();
} catch (e) { }