from thefuzz import process

#string matching classified character to their closest tagalog word
def recognize(output):
    #opening the txt files used to string matched
    a_file = open("tagalog_words.txt", "r")

    tagalog_words = []

    #adding every tagalog words in an array
    for line in a_file:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        tagalog_words.append(line_list)

    a_file.close()
    results = []
    sresults = []
    highest=[]
    shighest=[]
    output_length = len(output)
    
    word_count =3
    translated=""

    #string matching if character d occurs
    if output.find("d") !=-1:
        output_index = output.index('d')

        if output_index is not None:
            second_output = output.replace("d","r")
            print(second_output)
            Ratios = process.extract(output,tagalog_words, limit=5)
            SRatios = process.extract(second_output,tagalog_words, limit=5)

            if output_length <= 2:
                translated = 'Output: ' + output

            elif output_length > 2:
                for i in Ratios:
                    for j in i:
                        results.append(j)

                for k in SRatios:
                    for l in k:
                        sresults.append(l)
                

            
                del results[1::2]
                del sresults[1::2]
                print('hto', sresults)

                results = [ item for elem in results for item in elem]
                sresults = [ item for elem in sresults for item in elem]
              
                for x in results:
                    if len(x) > word_count:
                        #retrieving word with highest score of string matched
                        highest.append(x)

                for y in sresults:
                    if len(y) > word_count:
                        #retrieving word with highest score of string matched
                        shighest.append(y)

              
                translated = 'Written: ' +output + ' or ' + second_output +'\n Translated: ' +highest[0] + ' or ' + shighest[0]

    #string matching if character da is nonexistent
    else:
            
        #string matching the output to every items in the tagalog words array
        Ratios = process.extract(output,tagalog_words, limit=5)

        #No translation output if the written character is only one
        if output_length <= 2:
            translated = 'Output: ' + output

    
        #Translation output if character is more than one
        elif output_length > 2:
            for i in Ratios:
                for j in i:
                    results.append(j)
            del results[1::2]

            results = [ item for elem in results for item in elem]
            for x in results:
                if len(x) > word_count:
                    #retrieving word with highest score of string matched
                    highest.append(x)
            translated = 'Written: ' +output + '\n Translated: ' +highest[0]
    return translated
