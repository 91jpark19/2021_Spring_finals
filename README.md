# 2021_Spring_finals

## Does tree of democracy have been watered from blood? 

<p align="center">
    IS 597 Programing for Analytics & Data Processing (Type II Final Project)
</p>
 <p align="center">
  Jaihyun Park
</p>

![alt text](https://cdn.shopify.com/s/files/1/1877/6123/products/treeoflibertytee_1024x.jpg?v=1569159256)

**1. Motivation**

One of the great founding fathers Thomas Jefferson once said, "The tree of liberty must be refreshed from time to time with the blood of patriots and tyrants" in his [letter](//www.loc.gov/exhibits/jefferson/jefffed.html#105) to William Smith. The underlying meaning of his word cannot be understood without the context of historical background: oppression of British government and the struggle to earn independency. However, from what is being written, it also implies that the prosperity of one country accompanies sacrifices. This study examines whether the sacrifices arise from civil war can explain the changes of the level of democracy and liberty of one country.

**2. Literature Review**

In political science field, more narrowly in peace studies, the study on correlational relationship between institutional democracy can lead to world peace. One study from [Hegre et al. (2001)](https://www.jstor.org/stable/3117627?seq=1#metadata_info_tab_contents) suggested that intermediate regimes are prone to civil war, destabilizing political climate. The idea of Hegre et al. is often referred as 'Inverted U-Shape' to illustrate that semi-democracies (similar to intermediate regimes) experience more civil violence than autocracies and democracies ([Knutsen & Nygård, 2015](https://onlinelibrary.wiley.com/doi/full/10.1111/ajps.12168))

![alt text](https://github.com/91jpark19/2021_Spring_finals/blob/main/Images/inverted%20u-shape.JPG)

\<Figure 1: Inverted U-shape>

As \<Figure 1> from [Krishnarajan et al. (2016)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2822231) illustrates, where the democracy index is around 5 has the highest probability of starting the civil war. Even though prior research suggests that there is a relationship between the level of democracy and the likelihood of civil violence, their approach is different from this study's approach. While prior research explains the likelihood of civil violence with the level of democracy, this study explains how the level of democracy increased or decreased by fatalities.

**3. Hypotheses**

* H1. The changes of democracy score and the liberty score is not identical

* H2a. There is no relationship between the democracy score and the bloodshed due to civil war

* H2b. There is no relationship between the liberty score and the blood shed due to civil war

Listed above are the hypotheses that this study aims to answer. First hypothesis approaches to answer whether the democracy and liberty score of one country changes in the same way. This hypothesis will be helpful to demonstrate whether the country with free market also has democractic political system, although this is often thought to be true as history has seen. Building on the hypothesis 1, each of H2a and H2b centers around answering the question of correlational relationship between the either democracy or liberty score and fatalities of the civil war. This study operationalize the blood of patriots and tyrants as fatalities.

**4. Datasets**

[ICPSR](https://www.icpsr.umich.edu/web/pages/) is an institutional repository where the researchers who are affiliated with ICPSR publicize the dataset they used for the study for the sake of reproducibility. However, since ICPSR has rules that the data has to be accessed through ICPSR, this github repository does not uploaded the datasets being used. This study takes two datasets for [civil war data](https://doi.org/10.3886/ICPSR09905.v1) and [democracy data](https://doi.org/10.3886/ICPSR20440.v1). Anyone who are interested in replicating this study can access to the data by clicking it.

**5. Design Reasoning**

Fatalities (independent var) are normalized by total population at the moment of civil war. As changes in democracy score (dependent var) right after the end of the war is not sufficient to show changes in democracy score. Perhaps civil war has created the political instability and resulted in decreased in democracy level and liberty level. Therefore, this study measures 5 years, 10 years, and 20 years after the end of the war to consider the reconstruction period. In summary, independent variables are changes in democracy and liberty score with normalized fatalities as dependent variable. The level of analysis is civil war, not the country, meaning each data point represents the civil war. In addition, data with NAs in democracy, libery, and population score was removed.

**6. Preliminary Results of H1** 

|   Country   | Total Fatalities |
|:-----------:|:----------------:|
|    CHINA    |     3,497,525    |
| AFGHANISTAN |     1,064,000    |
|   NIGERIA   |     1,006,000    |
|     ...     |        ...       |
|   HONDURAS  |       1,000      |
|   SARDINIA  |       1,000      |
|  TAJIKISTAN |       1,000      |

\<Table 1: Total fatalities by country>

204 civil wars had occurred during 1816 - 1992 in 66 countries (SARDINIA has been removed from further analysis because it was not included in the democracy data). To answer hypothesis 1, this study conducted t-test in [scipy library](https://www.scipy.org/docs.html). p-value is used to explain whether the relationship is statistically meaningful with the threshold of 0.05. In the t-test, p-value greater than 0.05 means that the two groups are not identical. In this study, p-value greater than 0.05 means liberty score and democracy score have different patterns in changes. Among 65 countries, 62 countries had p-value less than 0.05. This indicates in most countries, democracy score and liberty score changes in the same direction. For example, if democracy score decreased, then liberty score also decreased. 

![alt text](https://github.com/91jpark19/2021_Spring_finals/blob/main/Images/NIGERIA.png)

\<Figure 2: Nigeria scores>

![alt text](https://github.com/91jpark19/2021_Spring_finals/blob/main/Images/UNITED%20STATES.png)

\<Figure 3: US scores>

\<Figure 2> shows an example from Nigeria, which had less than 0.05 for the p-value and <Figure 3> examplifies an example of greater than 0.05 p-value. United States, Bosnia and Herzegov, Finland, India, and Costa Rica had p-value larger than 0.05.

**7. Preliminary Results of H2**

|   Year  |   5  |  10  |   20  |
|:-------:|:----:|:----:|:-----:|
|  Slope  | 0.02 | 0.13 | -0.36 |
| p-value | 0.52 | 0.24 | 0.01* |

\<Table 2: Logistic regression on democracy score (H2a)>

|   Year  |   5  |  10  |   20  |
|:-------:|:----:|:----:|:-----:|
|  Slope  | 0.03 | 0.24 | -0.66 |
| p-value | 0.62 | 0.29 | 0.02* |

\<Table 3: Logistic regression on liberty score (H2b)>

After 20 years since the end of the civil war, the more fatalities that the civil war resulted in, the lower the democracy and liberty score become as shown in \<Table 2> and \<Table 3>. However, only 20-year gap observations shows statistical significance. Hypotheses are partially rejected, meaning bloodshed through civil war lowers the level of democracy and liberty in a long run. 

**8. Preliminary Conclusions**

* H1. Failed to Reject: changes of liberty and democracy score are identical in most of civil war-experienced countries.

* H2a. Partically Rejected: after 20 years since the end of civil war, democracy score tend to drop if there is more fatalities

* H2b. Partically Rejected: after 20 years since the end of civil war, liberty score tend to drop if there is more fatalities

**9. Limitations**
 
There are two limitations. One arise from the problem inherent in the dataset. First is incompleteness. Original data of [civil war data](https://doi.org/10.3886/ICPSR09905.v1) contained many missing values. Furthermore, TAJIKISTAN was labeled as TAKJIKISTAN in [civil war data](https://doi.org/10.3886/ICPSR09905.v1), which might have been neglected without close inspection. At the same time, [democracy data](https://doi.org/10.3886/ICPSR20440.v1) had missing values in the population column. Aside from incompletness of two datasets, another problem is incompatability. [civil war data](https://doi.org/10.3886/ICPSR09905.v1) contained SARDINA, which is not included in [democracy data](https://doi.org/10.3886/ICPSR20440.v1).

The second limitation is a method-wise limitation. This study did not control confounding factors. There may be other factors resulted in lowering the level of democracy. Perhaps, decreased population due to severe civil war may have influenced the delay of improving democracy level. Another concern hinges on intermediate variables. civil violence may have resulted in infrastructural disruption and infrastructural disruption resutled in delays in improving democracy level. This intermediate variables are not considered in this study. Last but not least, the country is not a permanent entity that does not divide or unite. In this study, the civil war happened while AUSTRIA-HUNGARY exists has been copyed and added to both AUSTRIA and HUNGARY. Depending on how to control the changes in country's name and how the study consider its history, the result may vary. 
