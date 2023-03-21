# Codewars Activity Chart

> Also check [CodewarsLogger](https://github.com/JoseDeFreitas/CodewarsLogger)!

This is a little program that prints a chart, in the form of a calendar (based
on the year you choose),[^1] that shows the days a specified user completed katas
in Codewars and the quantity of the katas they completed in that day. The API also
counts the total amount of katas completed in the year and the streak of completion.[^2]
Head to the [Screenshots](#screenshots) section to see how it looks. **The contribution
chart from GitHub was my inspiration.**

Charts like this exist in some websites. Although they look cool, I don't think
they provide anything useful, and, in some cases, I believe they're noxious as
force you to keep contributing (even if you don't want to) or preserve a streak
that is, pretty much, useless. This may not seem like an issue, but I do believe
it's wrong to make a change (in any website) just to keep the chart "pretty".
It's not that of a big deal as it's up to you not to pay attention to the chart
and stop doing useless changes, but it's still an incentive to do so.

This program serves only as a cool statistical graph. I recommend you practise your
coding skills when you want and as you want, not to keep the chart full.

## Screenshots

<a href="https://codewars-activity-chart.glitch.me/jhoffner?year=2013"><img alt="Codewars Activity Chart example" src="https://user-images.githubusercontent.com/37962411/226577099-7de8863c-9044-4b4b-941f-b2e175d09435.png" height="404"/></a>

## Usage

To get the chart, simply go to **https://codewars-activity-chart.glitch.me** and
add the required parameters. Below you can find the list of the available path
and query parameters, as well as some examples. If the user couldn't be found or
there is no katas completed for the choosen year, the API will let you know with
a red message.

To see the amount of katas completed in a day, you must hover over that day.

### Parameters

| Parameter          | Required | Default value    | Example                                                               |
| ------------------ | -------- | ---------------- | --------------------------------------------------------------------- |
| username           | yes      |                  | https://codewars-activity-chart.glitch.me/jhoffner                    |
| year               | no       | Current year     | https://codewars-activity-chart.glitch.me/jhoffner?year=2016          |

### Embedding

You can embed the chart in your website (or any website that allows for embedding
other websites) using the [`<iframe>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe)
tag from HTML:

```html
<iframe src="CHART_URL" width="625" height="421"></iframe>
```

625 of width and 421 of height looks good enough to show only the chart, but you
can tweak these values as you want.

## Remarks

- The JSON data that you get from the [Codewars API](https://dev.codewars.com/)
contains a maximum of 200 katas completed per page. It needs to make new calls
to retrieve all of the katas that a user completed, and that's what the program
does. If you have completed a massive amount of katas, it may take some time, but
I believe it's not of a big deal. **Please, don't overwhelm the API**.
- When no one has made a request to the website in 5 minutes, Glitch (the host
I'm using) turns off the website. In this case, you'll need to wait some seconds for
the chart to appear. There is also a [limited amount of hours per month](https://help.glitch.com/kb/article/17-technical-restrictions/)
for the free plan (which is the one I'm using).
- The timezone used by the program is **UTC**. This is because it's faster this way
for the user to get the chart (as he would need to also type in the timezone they
want). However, I may introduce the feature to select a specific timezone in the
future.
- You **have to** embed it in another page for it to show. I tried generating the
image directly in PNG or SVG (without the use of any third-party library), but it was
too messy.

[^1]: The shape of the months are different from one another because, instead of
printing the days as GitHub does, it prints them like a normal calendar. You can
see the day of the week by counting the row the day is in. It starts at Monday and
finishes at Sunday.
[^2]: If you choose the current year, it will print the current streak. If you
choose any other year that has already passed, it will print the longest streak
made.
