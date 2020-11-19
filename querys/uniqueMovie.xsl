<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="2.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="movie">
        <h1 style="text-align: center;padding-top:2%;font-size:57px;"><b><xsl:value-of select="original-title"/></b></h1>
        <div class="film-card" style="padding-top: 3%;">
            <img class="image-card_1" style="padding-left:17.5%">
                <xsl:attribute name="src">
                    <xsl:value-of select="cover-url"/>
                </xsl:attribute>
            </img>
            <div class="rating-card_1" >
                <h1> <xsl:value-of select="rating"/>/10</h1>
                <h6>Number of votes: <xsl:value-of select="votes"/> </h6>
            </div>
            <div style="padding-left:3%;">
                <h2><b>Stars:</b>
                    <xsl:variable name="count1" select="4"/>

                    <xsl:for-each select="cast/person">
                        <xsl:if test="position() &lt; $count1">
                            <xsl:value-of select="name"/>
                            <xsl:if test="position() != 3">
                                <xsl:text>,</xsl:text>
                            </xsl:if>
                        </xsl:if>
                    </xsl:for-each>
                </h2>
                <h2><b>Directors:</b> <xsl:for-each select="directors"> <xsl:value-of select="person/name" separator=","/></xsl:for-each> </h2>
                <h2><b>Writers:</b> <xsl:for-each select="writers"> <xsl:value-of select="person/name" separator=","/></xsl:for-each> </h2>
                <h3><b>Runtime :</b> <xsl:value-of select="runtimes/item"/> min</h3>
                <h3><b>Genres:</b> <xsl:for-each select="genres"> <xsl:value-of select="item" separator=","/></xsl:for-each></h3>
                <div class="last_div">
                    <h4><b>Original Air Date: </b><xsl:value-of select="original-air-date"/></h4>
                    <h4><b>Languages: </b><xsl:value-of select="languages" /></h4>
                </div>
            </div>
        </div>




        <div class="col-sm-8 " style="left:16.5%; padding-bottom:2%;">
            <xsl:variable name="count" select="11"/>
            <table style="padding-top: 15%;">
                <tr>
                    <th>Actor</th>
                    <th>Characters</th>
                </tr>
                <xsl:for-each select="cast/person">
                    <xsl:if test="position() &lt; $count">
                    <tr>
                        <td><xsl:value-of select="name"/></td>
                        <td><xsl:value-of select="current-role/character/name"/></td>
                    </tr>
                    </xsl:if>
                </xsl:for-each>
            </table>
        </div>
        <div class="col-sm-8 " style="left:16.5%;">
            <xsl:if test="plot-outline != ''">
                <h4><b>Plot:</b><p> <xsl:value-of select="plot-outline"/></p></h4>
            </xsl:if>
            <xsl:if test="plot//item != ''">
                <h4><b>Synopsis:</b> <p><xsl:value-of select="plot//item"/></p></h4>
            </xsl:if>
        </div>
    </xsl:template>

</xsl:stylesheet>