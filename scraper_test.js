const puppeteer = require('puppeteer');
//const url = 'https://www2.gov.bc.ca/gov/content/governments/services-for-government/information-management-technology/records-management/information-schedules/arcs/administrative-records/general';
const url = 'https://www2.gov.bc.ca/gov/content/governments/services-for-government/information-management-technology/records-management/information-schedules/arcs/financial-records/fees';

if (!url) {
    throw "Please provide URL as a first argument";
}

function run () {
    return new Promise(async (resolve, reject) => {
        try {
            const browser = await puppeteer.launch();
            const page = await browser.newPage();
            await page.goto(url);
            
            // set an index to track pages downloaded
            let currentPage = 1;
            let isNext = true;
            let data = [];
            while (isNext){
                // process each page
                currentPage += 1;
                let newData = await page.evaluate(() => {
                    let pageTitle = document.title;
                    
                    var pageNext, pagePrev, pageText;

                    // get the page text describing the primary
                    let results = [];
                    let bs = document.querySelector('div#body');
                    let ps = Array.from(bs.children);
                    let pidx  = 1; // for some reason it is +1
                    ps.forEach((p, idx) => {
                        console.log(p.tagName)
                        pidx += 1;
                        let links = p.querySelectorAll('a');
                        let clickFound = false;
                        if (links.length > 0){
                            let lidx = 0;
                            links.forEach((l) => {
                                lidx += 1;
                                if (l.innerText === 'Next'){
                                    pageNext = 'div#body > p:nth-child(' + ps.length + ') > a' + ((links.length > 1) ? ':nth-child(' + lidx + ')': ''); // 
                                    clickFound = true;
                                } else if (l.innerText === 'Previous'){
                                    clickFound = true;
                                }
                            });
                        } 
                        
                        if (!clickFound && p.tagName != 'TABLE')
                        {

                            results.push(p.innerText);    
                        }
                    });
                    pageText = results.join('\n');

                    // extract the secondaries from a table...
                    let dr = document.querySelectorAll('div#body > table > tbody > tr');
                    let pageData = []
                    dr.forEach((r) => {
                        let cells = r.querySelectorAll('td');
                        if (cells.length >= 5 ){
                            pageData.push({
                                series: cells[0].innerText,
                                text: cells[1].innerText,
                                a: cells[2].innerText,
                                sa: cells[3].innerText,
                                fd: cells[4].innerText,
                            })
                        }
                    });

                    // sort the items out and return...
                    return {
                        title: pageTitle,
                        text: pageText,
                        next: pageNext,
                        previous: pagePrev,
                        data: pageData,
                    };
                }); // newData
            
                data.push(newData);

                // loops to next page...
                //*[@id="body"]/p[5]/a[2]
                //document.querySelector("#body > p:nth-child(6) > a")
                //document.querySelector("#body > p:nth-child(5) > a:nth-child(2)")
                
                // #body > p:nth-child(6) > a
                // #body > p:nth-child(5) > a:nth-child(2)
                let selText = 'next';
                console.log(newData['title']);
                //console.log(newData[selText]);
                if (newData[selText]){ //   
                    // click to next page
                    //console.log('Next...')
                    await Promise.all([
                        await page.click(newData[selText]),
                        await page.waitForSelector('div#body')
                    ])
                } else {
                    console.log('Finished....')
                    isNext = false;
                }
            }

            // close and return
            browser.close();

            // save to file
            var fs = require('fs');
            fs.writeFile('arcsdata.json', JSON.stringify(data, null, 2), 'utf8', function (err) {
                if (err) throw err;
                console.log('Saved!');
            });        
    
            // return data
            return resolve(data);
        } catch (e) {
            return reject(e);
        }
    })
}

// run and print output...
run().then(console.log).catch(console.error);