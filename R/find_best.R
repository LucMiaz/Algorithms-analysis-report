find_best<-function(tff, plotName='figures/plotname.pdf', authors=unique(tff$author), qualities=unique(tff$quality)){
  bestones<-data.frame('TPR'=double(),'FPR'=double(),'thd'=double(),'totP'=double(), 'totF'=double(),'alg'=character(),'algprop'=character(), 'delta'=double())
  #iterate on algorithms
  for (al in unique(tff$alg)){
  #iterate on parameters
    for (alp in unique(tf$algprop)){
      sums<-data.frame('TPR'=double(),'FPR'=double(),'thd'=double(),'totP'=double(), 'totF'=double(), 'delta'=double())
      algtf<-filter(tff, algprop==alp & alg==al)
      #iterate on thresholds
      #thresholds<-seq(min(algtf$spec),max(algtf$spec),(max(algtf$spec)-min(algtf$spec))/200)
      thresholds<-seq(-1,10,0.1)
      delta<-thresholds[[2]]-thresholds[[1]]
      for (i in thresholds){
        TP<-tally(filter(algtf, spec<=i & disc==1 & author %in% authors & quality %in% qualities))
        FP<-tally(filter(algtf, spec<=i & disc==0& author %in% authors & quality %in% qualities))
        totP<-tally(filter(algtf,disc==1& author %in% authors & quality %in% qualities))
        totF<-tally(filter(algtf,disc==0& author %in% authors & quality %in% qualities))
        if (totP>0 & totF>0){
          sums[nrow(sums)+1,]<- data.frame('FPR'=FP/totF, 'TPR'=TP/totP, 'thd'=as.numeric(i), 'totP'=totP, 'totF'=totF)
        }
      }
      thresmax<-which.max(abs(sums$TPR-sums$FPR))
      bestones <-rbind(bestones,data.frame('TPR'=sums$TPR[thresmax],'FPR'=sums$FPR[thresmax],'thd'=sums$thd[thresmax],'totP'=sums$totP[thresmax],'totF'=sums$totF[thresmax], 'alg'=al[[1]],'algprop'=as.character(alp[1]),'delta'=delta))
      remove(sums,thresmax)
    }
  }
  remove(FP,TP,totP,totF,algtf,thresholds,al,alp)
  bestones<-cbind(bestones, data.frame('col'=as.integer(bestones$algprop)))
  
  bestones<-bestones[mixedsort(bestones$algprop),]
  bestones<-cbind(bestones, data.frame('dif'=bestones$TPR-bestones$FPR))
  rocplot <- ggplot(bestones, aes(bestones$FPR,bestones$TPR,color=bestones$algprop, title='Algorithms'))+  geom_segment(aes(x =0, y = 0, xend = 1, yend = 1), colour="#a5a5a5")+
    scale_colour_manual(values=rep(brewer.pal(12,"Paired"),times=2),name="Algorithms")+
    scale_shape_manual(values=rep(c(15,16,3,17,18,19),each=3),name="Algorithms")+
    geom_point(aes(shape=bestones$algprop,label=bestones$algprop),size=2)+
    xlab("False Positive Rate") + ylab("True Positive Rate")+
    labs("ROC")
  
  #geom_point(aes(sums$n[thd==thres],sums$n.1[thd==thres]), colour="#7b3294", size=3, label=thres)
  #geom_text(data=filter(sums,thd==thres),aes(label=thd))
  returnlist<- list('plot'=rocplot, 'bestframe'=bestones)
  ggsave(plotName, plot=rocplot,  width=8, height=6)
  return(returnlist)
}