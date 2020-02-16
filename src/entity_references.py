import re

def __decode_entity_references_into_utf8(entity_references):
    num_list = re.findall(r'\&#(\d+);',entity_references)
    
    code = 0
    for n in num_list:
        if code == 0:
            code = int(n)
        else:
            code = code << 8 | int(n)

    if len(num_list) == 1:
        char = chr(code)
    else:
        char = code.to_bytes(len(num_list),'big').decode('utf-8')
    
    return char

def __make_mojibake_char(entity_references):
    num_list = re.findall(r'\&#(\d+);',entity_references)
    
    for n in num_list:
        print('_{}'.format(chr(int(n))))

def __get_entity_references(html):
    return re.findall(r'((?:\&#\d+;)+)',html)

def __get_dict_of_entity_reference_and_utf8(ref_list):
    utf8_dict = {}
    for ref in ref_list:
        char = __decode_entity_references_into_utf8(ref)

        # convert nbsp into space
        if char == '\xa0':
            char = ' '

        utf8_dict[ref] = char
    
    return utf8_dict


def change_entity_references_to_utf8_in_text(text):
    ref_list = __get_entity_references(text)
    utf8_dict = __get_dict_of_entity_reference_and_utf8(ref_list)

    replace_text = text
    for ref, utf8 in utf8_dict.items():
        replace_text = replace_text.replace(ref, utf8)
    
    return replace_text

if __name__=='__main__':
    
    html = '''<div class="section-paragraph">The three-dimensional structures of chromosomes are increasingly being recognized
         as playing a major role in cellular regulatory states. The efficiency and promiscuity
         of phage Mu transposition was exploited to directly measure
         <em>in&#194;&#160;vivo</em> interactions between genomic loci in
         <em>E.&#194;&#160;coli</em>. Two global organizing principles have emerged: first, the chromosome is well-mixed
         and uncompartmentalized, with transpositions occurring freely between all measured
         loci; second, several gene families/regions show &#226;&#128;&#156;clustering&#226;&#128;&#157;: strong three-dimensional
         co-localization regardless of linear genomic distance. The activities of the SMC/condensin
         protein MukB and nucleoid-compacting protein subunit HU-α; are essential for the well-mixed
         state; HU-α; is also needed for clustering of 6/7 ribosomal RNA-encoding loci. The
         data are explained by a model in which the chromosomal structure is driven by dynamic
         competition between DNA replication and chromosomal relaxation, providing a foundation
         for determining how region-specific properties contribute to both chromosomal structure
         and gene regulation.
      </div>'''
    
    ref_list = __get_entity_references(html)
    utf8_dict = __get_dict_of_entity_reference_and_utf8(ref_list)
