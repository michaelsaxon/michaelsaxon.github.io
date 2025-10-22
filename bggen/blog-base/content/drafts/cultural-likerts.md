Title: Potential problems with using Likert scales cross-culturally
Date: 2025-10-21 17:45
Category: Research
Tags: Evaluation, Culture
Authors: Michael Saxon
Summary: Extracted and expanded section from our EMNLP 2025 paper on issues with cultural evaluation.
Image: images/grfp.jpg
Status: draft

In our EMNLP 2025 paper "[Culture is Everywhere: A call for intentionally cultural evaluation](https://arxiv.org/pdf/2509.01301)" we talk about a grab bag of issues with cultural NLP research from an HCI-flavored perspective.
I mainly worked on section 3, "How to evaluate."
While we were drafting this one of the questions I was interested in checking is, *do cultural differences change the intended meaning behind equivalent responses?* In other words, if a Brit and an American both give a 3/5 rating for satisfaction after interacting with an AI system (or in any study), do those mean the same thing?
I suspected the answer is[^1] no.

[^1]: By *is*, what I really mean here is *can be*.

So I looked in to examples of this phenomenon in academic research and in general public discussions. To my surprise, this is pretty understudied!
There are a few academic results, mainly in education studies, with one reference I could find in education.
I think this is a ripe area for future study as it has important implications for evaluation.

# Academic results
[RESPONSE STYLE AND CROSS-CULTURAL COMPARISONS OF RATING SCALES AMONG EAST ASIAN AND NORTH AMERICAN STUDENTS](https://escholarship.org/content/qt1b00n182/qt1b00n182.pdf?t=nqcr5a)

> Responses to fifty-seven 7-point Likert-type scales were analyzed. The Japanese and Chinese students were more likely than the two North American groups to use the midpoint on the scales; the U.S. subjects were more likely than the other three groups to use the extreme values. Within each cultural group, endorsement of individualism was positively related to the use of extreme values and negatively related to the use of the midpoint.

This difference that they find is statistically significant, and can be described as between the East Asian (from Japan and Taiwan) students and North American students (from US and Canada), not a strictly country-level difference (although preference for extreme points was more pronounced in the Americans)

[Cultural differences in responses to a Likert scale](https://pubmed.ncbi.nlm.nih.gov/12124723/)

> [*Chinese and Japanese respondents*] more frequently on items that involved admitting to a positive emotion than did the Americans, who were more likely to indicate a positive emotion.

[Do Country and Culture Influence Online Reviews? An Analysis of a Multinational Retailer’s Country-Specific Sites](https://www.tandfonline.com/doi/full/10.1080/08961530.2019.1635552)

- Compare FR, DE, UK, US, JA Amazon reviews. 
- Mean reviews in western countries are all $4.26 \pm 0.3$, while the mean Japanese score is 3.57. 
- Mean "Review was helpful" vote rate in western countries was $65\pm4\%$ while in Japan was 75%. 
- This highlights how cultural differences in negative response bias and extreme response bias drive single-unrelated-item incomparability between countries

[Understanding the Impact of Culture in Assessing Helpfulness of Online Reviews](https://www.semanticscholar.org/reader/4aa7af6a99000048b8bfb322ef42e4024c2a7b39)
- In the ACM social media studies literature
- Similar result to above but for Arabic vs English
- Category-specific differences in hotel reviews and book reviews
- In hotel reviews the difference between extreme and mid response biases shows up, with Arabic reviewers also exhibiting a relative hesitance to provide 5-star reviews

[Extreme Response Style in Cross-Cultural Research](https://www.semanticscholar.org/paper/Extreme-Response-Style-in-Cross-Cultural-Research-Chun-Campbell/ba5f88cc1f734836d0540c906def60e623d11bfc)
- Early discussion of the existence of ERS and that ignoring it confounds comparisons of genuine group differences
	- Tbh, I think this completely calls into question the value of international happiness studies for ex
- They compare Korean and American university students on interpersonal and sociopolitical trust
- Relative lack of extreme response bias in Korean students *renders their extreme responses more "reliable" wrt consistent agreement*

## Caveats
Results showing that differences are still correlated?

The differences are still correlated. In some applications, all we need is a correlation and this isn't a problem. However if we are for example comparing the absolute satisfaction level between populations this becomes important.


# Non-academic discussion
Excerpted from a deleted [OpenAI employee tweet](https://x.com/georgejrjrjr/status/1917722125668081863):

> there's another old story i heard about how an early GPT model stopped speaking Croatian one week and nobody could figure out why. turns out Croatian users were much more prone to downvote messages so the model just gave up and decided to not speak Croatian anymore.

This effect has been memed before, such as in this example about interface feedback:

![]({attach}images/culturalresponse.jpeg)

This effect also plays out in restaurant ratings, from the [Japan Times](https://www.japantimes.co.jp/life/2025/03/09/food-drink/tabelog-ratings-cultural-influences/):

> “Tabelog users tend to not give high ratings just because they find a (restaurant’s food) delicious but rather ... they tend to rate restaurants carefully, considering them in relation to other renowned establishments,” he says.

> “(It could) also be an ability to want to see things both ways or to not stand out too much from others,” says Farrer. “This means Japanese people are somewhat more likely to choose a three rather than a one or a five.”


A [tourism guide](https://www.japantravelpros.com/blog/star-ratings-reviews-japan-is-different ) reports an (unscientific) description of the impacts of this trend:

> **As the number of English reviews increases, the reliability decreases**... A popular chain of conveyor belt sushi eateries in Japan would be a great example. One of its locations, in a neighborhood in Tokyo that’s very popular among tourists, has a **4.3**-star rating. Another location, in a quiet, rural area of Hyogo prefecture, has a **3.2**-star rating. This chain goes through strict measures to ensure **product and service consistency** across its locations, and yet look at the **discrepancy in ratings**!