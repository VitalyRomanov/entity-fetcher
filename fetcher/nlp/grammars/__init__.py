class HearstNpEnGrammar:
    grammar = r"""
        # NP:
        #     {<DET>?<NOUN|ADJ><NOUN|ADJ|'s|of|in|with|for|on|over|throughout>*<NOUN>}
        SRV_kind_of:
            {<.*_kind><.*_of>}
        SRV_such_as:
            {<.*_such><.*_as>}
        SRV_and_other:
            {<.*_and><.*_other>}
        SRV_as_well_as:
            {<.*_as><.*_well><.*_as>}
        NP_name:
            {<.*_dr><\.>?<NOUN>*}
        NP:
            {<DET>?<NOUN|ADJ|.*_'s>*<NOUN>}
        NP_of:
            {<NP><.*_of><NP>}
        NP_in:
            {<NP><.*_in><NP>}
        NP_with:
            {<NP><.*_with><NP>}
        NP_for:
            {<NP><.*_for><NP>}
        NP_on:
        # maybe this rule should only work in subconcepts
            {<NP><.*_on><NP>}
        NP_over:
            {<NP><.*_over><NP>}
        NP_throughout:
            {<NP><.*_throughout><NP>}
        """

class HearstNpRuGrammar:
    grammar = r"""
        SRV_v_tom_chisle:
            {<.*_в><.*_том><.*_числе>}
        SRV_pod_rukovodstvom:
            {<.*_под><.*_руководством>}
        SRV_takie_kak:
            {<.*_такие><.*_как>}
        SRV_takih_kak:
            {<.*_таких><.*_как>}
        SRV_takimi_kak:
            {<.*_такими><.*_как>}
        SRV_takim_kak:
            {<.*_таким><.*_как>}
        SRV_i_drygiye:
            {<.*_и><.*_другие>}
        SRV_i_drygih:
            {<.*_и><.*_других>}
        SRV_i_drygimi:
            {<.*_и><.*_другими>}
        SRV_i_drygim:
            {<.*_и><.*_другим>}
        SRV_v_chasnosti:
            {<.*_в><.*_частности.*>}
        SRV_razlichnyh:
            {<.*_в><.*_различны.*>}
        SRV_t_d_p:
            {<.*_т\.><.*_д\.|.*_п\.>}
        NP_adj_noun: 
            {<ADJ_nomn.*>{1,}<NOUN_nomn.*>}
        NP_adj_noun: 
            {<ADJ_gent.*>{1,}<NOUN_gent.*>}
        NP_adj_noun: 
            {<ADJ_datv.*>{1,}<NOUN_datv.*>}
        NP_adj_noun: 
            {<ADJ_accs.*>{1,}<NOUN_accs.*>}
        NP_adj_noun: 
            {<ADJ_ablt.*>{1,}<NOUN_ablt.*>}
        NP_adj_noun: 
            {<ADJ_loct.*>{1,}<NOUN_loct.*>}
        NP_adj_noun: 
            {<ADJ_accs.*>{1,}<NOUN_nomn.*>}
        NP_noun_noun_s: 
            {<NOUN_nomn.*>{1,}<NOUN_nomn.*>}
        NP_noun_noun_s: 
            {<NOUN_gent.*>{1,}<NOUN_gent.*>}
        NP_noun_noun_s: 
            {<NOUN_datv.*>{1,}<NOUN_datv.*>}
        NP_noun_noun_s: 
            {<NOUN_accs.*>{1,}<NOUN_accs.*>}
        NP_noun_noun_s: 
            {<NOUN_ablt.*>{1,}<NOUN_ablt.*>}
        NP_noun_noun_s: 
            {<NOUN_loct.*>{1,}<NOUN_loct.*>}
        NP_noun_noun_none_s: 
            {<NOUN_None.*>{1,}<NOUN_None.*>}
        NP_adj_noun_q:
            {<ADJ.*>{1,}<NOUN.*>}
        NP_noun_noun_q:
            {<NOUN.*>{1,}<NOUN.*>}
        NP_noun:
            {<NOUN.*>}
        NP_adj:
            {<ADJ.*>}
        NP_at:
            {<NP.*><.*_на><NP.*>}
        NP_at:
            {<NP.*><.*_в><NP.*>}
        """

class HearstEnPatterns:
    # TODO:
    # 1. Pattern 1: NP such as NP and NP, NP, NP and NP, where first NP and NP is actually one NP
    #     After the Forum completed its basic standard reference architecture, as of May 2018, it reportedly completed ten international blockchain standards such as terminology and concepts, reference architecture, classification and ontology, which have now entered development stage.
    #     Some sources familiar with the matter believed that cancellation of the planned ICO can be a result of increasingly strict regulations that are proposed by such entities as the Securities and Exchange Commission, Commodity Futures Trading Commission, and others since the company initially began examining a possibility to launch its ICO.
    # 2. Pattern 1: Sometimes tail of pattern 1 is an auxiliary sentence
    #     However, over the past six months, as he has learnt more about Ripple and XRP (perhaps, partly due to conversations with Ripple employees, such as CTO David Schwartz, and famous XRP fans such as Michael Arrington, the co-founder of digital asset management firm Arrington XRP Capital), hate seems to have gradually turned into love.
    # 3. Pattern 2: Create grammar pattern for no such so that it does not participate in target patterns
    # 4. Pattern 2: filter "such a", because it has different meaning
    # 5. Pattern 2: does not always work. Maybe need to try classifying before parsing
    #       The law requires that salaried workers who earn a minimum of 200,000 yen from cryptocurrency trading and investing annually to declare such earnings as income
    #       It’s fair to describe such behavior as a bet, as no one can predict where the market is going, but if you’re experienced and have insight into crypto movements, futures could prove indispensable.
    #       Explaining how the privacy-focused capabilities of Zcash will be supported on Coinbase, the company revealed that it would offer partial support for shielded transactions until such a time as local regulations allow for full implementation of transaction shielding.
    #       The move to open source the code indicates that Bitmain may not necessarily be offering such services as part of its core business model moving forward.
    #       They declared all such fundraising-related activities as illegal.
    # 6. Patter 3: Does not always work
    #       In addition to this, the binaries are available in many options including Solaris, Plan 9, and BSD operating systems.
    #       Since the acrimonious fork, a lot has happened within the BCH ecosystem including a few exchanges listing both chains as separate coins.
    #       Kraken has warned customers that the SV chain does not meet the company’s traditional listing requirements for a variety of reasons including the fact that it has “no known wallets supporting replay protection, miners are operating at a loss, and representatives threatening and openly hostile toward other chains.” Additionally, the exchange said it has completed only a small amount of code review and stressed that “large holders have indicated they’d be dumping everything.”
    #       Ping An Bank is undergoing a series of business changes under the auspices of financial technology, including the use of artificial intelligence (AI), big data, blockchain, and cloud computing in order to “ensure low-cost, efficient and personalized public services,” the People’s Daily reports.
    # 7. Patter 4: Does not always work
    #       Also, keep up with your holdings, BCH and other coins, on our market charts at Satoshi’s Pulse, another original and free service from Bitcoin.com.
    #       Mir, an international broadcasting corporation with several Russian language TV channels, a radio station and an online outlet, is launching a new program that will inform viewers about digital coins, mining and other related technologies.
    #       Based on current market conditions and the intensity of the drop over the last 24 to 48 hours, Bitcoin Cash and other major cryptocurrencies are expected to drop further in price, with BCHABC eyeing a test of $180 for the first time in its 15-month history.
    #       According to a letter released by the Institute for Business and Social Impact (IBSI), which is to work with the Masters of Financial Engineering (MFE) program at Berkeley, dictates that the grant will finance the faculty, student research and other related activities across the Berkeley Campus.
    # 8. Pattern 5: Some bugs: did not parse last entity
    #       Its major dominance is in the Asian market especially South Korea, Singapore, and Japan.
    # 9. When having composed NP (NP in NP and such) most of the time we need to select only one NP as target concept
    #       It is pretty impossible to do this with grammars, e.g. 'payments for major companies such as google'
    #       Can try to resolve this using word vectors. What is the concept that is the closest to all subconcepts
    #       For some it is easy to decide: forms of capital -> equity
    # 11. Exclude 'and other'
    grammar = r"""
        NP:
            {<DT>?<JJ>*<NN.*>}
        NP:
            {<U-NP>}
        NP:
            {<B-NP>(<I-NP>)*<L-NP>?}
            # {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        NP:
            {(<I-NP>)*<L-NP>?}
        NP:
            {<L-NP>}
        NP:
            {<I-NP>}
        P1:
            {<NP.*><.*_such><.*_as>(<NP.*><.*_,>)*(<NP.*><.*_and|.*_or>)?<NP.*>}
        P1:
            {<NP.*><SRV_such_as>(<NP.*><.*_,>)*(<NP.*><.*_and|.*_or>)?<NP.*>}
        P2:
            {<.*_such><NP.*><.*_as>(<NP.*><.*_,>)*(<NP.*><.*_and|.*_or>)?<NP.*>}
        P3:
            {<NP.*><.*_,>?<.*_including>(<NP.*><.*_,>)<SRV_as_well_as>(<NP.*><.*_and|.*_or>)?<NP.*>}
        P3:
            {<NP.*><.*_,>?<.*_including>(<NP.*><.*_,>)*(<NP.*><.*_and|.*_or>)?<NP.*>}
        P4:
            {<NP.*>(<.*_,><NP.*>)*<.*_,>?<.*_and><.*_other><NP.*>}
        P4:
            {<NP.*>(<.*_,><NP.*>)*<.*_,>?<SRV_and_other><NP.*>}
        P5:
            {<NP.*><.*_,>?<.*_especially>(<NP.*><.*_,>)*(<NP.*><.*_and|.*_Por>)?<NP.*>}
        """

class HearstRuPatterns:
    # TODO
    # 1. This sentence will generate incorrect candidates
    #       В Северном районе к основным отраслям относятся добыча угля, нефти, газа, апатитов, никеля и других металлов, а также заготовка леса и ловля рыбы.
    #       Конституция гарантирует «свободу совести, свободу вероисповедания, включая право исповедовать индивидуально или совместно с другими любую религию или не исповедовать никакой, свободно выбирать, иметь и распространять религиозные и иные убеждения и действовать в соответствии с ними».
    grammar = r"""
        NP:
            {<NOUN>*<ADJ>*<NOUN.*>}#{<NOUN.*|ADJ>*<NOUN.*>}  # add NONLEX for foreign names
        NP:
            {<U-NP>}
        NP:
            {<B-NP>(<I-NP>)*<L-NP>?}
        NP:
            {(<I-NP>)*<L-NP>?}
        NP:
            {<L-NP>}
        NP:
            {<I-NP>}
        P1:
            {<NP.*><.*_,>?<.*_такие|.*_таких|.*_такими><.*_как>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>} # а так же;
        P1_nomn:
            {<NP.*><.*_,>?<SRV_takie_kak>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>}
        P1_gent_accs_loct:
            {<NP.*><.*_,>?<SRV_takih_kak>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>}
        P1_datv:
            {<NP.*><.*_,>?<SRV_takim_kak>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>}
        P1_ablt:
            {<NP.*><.*_,>?<SRV_takimi_kak>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>} 
        P2:
            {<.*_такие|.*_таких|.*_такими><NP.*><.*_,>?<.*_как>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>} #таких фильмах режиссера, как «Человек ниоткуда», «Вокзал для двоих» и «Старые клячи»
        P3:
            {<NP.*><.*_,>?<.*_включая>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>}
        P4:
            {<NP.*>(<.*_,><NP.*>)*<.*_,>?<.*_и><.*_другие|.*_других|.*_другими><NP.*>}
        P4_nomn:
            {<NP.*>(<.*_,><NP.*>)*<.*_,>?<SRV_i_drygiye><NP.*>}
        P4_gent_accs_loct:
            {<NP.*>(<.*_,><NP.*>)*<.*_,>?<SRV_i_drygih><NP.*>}
        P4_datv:
            {<NP.*>(<.*_,><NP.*>)*<.*_,>?<SRV_i_drygim><NP.*>}
        P4_ablt:
            {<NP.*>(<.*_,><NP.*>)*<.*_,>?<SRV_i_drygimi><NP.*>}
        P5:
            {<NP.*><.*_,>?<.*_особенно>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>} # Откуда у людей, особенно у женщин, такой менталитет?
        P6:
            {<NP.*><.*_,>?<.*_в><.*_частности>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>} # kill
        P6:
            {<NP.*><.*_,>?<SRV_v_chasnosti>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>} # kill

        # и другие, а так же другие
        """
