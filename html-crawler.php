<?php

namespace MortgageCrawler;

use Symfony\Component\DomCrawler\Crawler;
use GuzzleHttp\Client;
use GuzzleHttp\Exception\RequestException;
use GuzzleHttp\Exception\ClientException;

class HmlCrawler
{
    
    
    public function crawlLinkFromHtml($html) {
    
        $crawler = new Crawler($html);
            
        $nodes = $crawler->filter('.contacts-list a');
        $links = [];
        foreach($nodes as $node) {
            $link = trim($node->getAttribute('href'));
            if (empty($link)) {
                continue;
            }
            $links[] = $link;
        }

        return $links;
    }


    public function crawlInfoFromLink($url) {
        $error = '';
        try {

            $client = new Client();
            
            $html = $client->get($url)->getBody()->getContents();
            
            $crawler = new Crawler($html);
            
            $name = $crawler->filter('.banner-contact-info .banner-primary-text')->text();
            $names = explode(" ", $name);
            $first_name = !empty($names[0]) ? $names[0] : '';
            $last_name = !empty($name) ? str_replace($first_name." ", "", $name) : '';
            
            $nmls = $crawler->filter('.banner-contact-info .banner-secondary-text')->text();
            $nmls = str_replace("NMLS #", "", $nmls);
            $contacts = [];
            $nodes = $crawler->filter('.contact-info-list li a');
            foreach($nodes as $i => $node) {
                $contacts[] = trim($node->textContent);
            }
            $address = !empty($contacts[0]) ? $contacts[0] : '';
            $address_list = explode(" ", $address);
            $len = count($address_list);
            $zip = !empty($address_list[$len-1]) ? $address_list[$len-1] : '';
            $state = !empty($address_list[$len-2]) ? $address_list[$len-2] : '';
            
            $phone = !empty($contacts[1]) ? $contacts[1] : '';
            $website_url = !empty($contacts[2]) ? $contacts[2] : '';

            $nodes = $crawler->filter('.social-links-list li a');
            $socials = [];
            foreach($nodes as $i => $node) {
                $socials[] = trim($node->getAttribute('href'));
            }
            $facebook_url = !empty($socials[0]) ? $socials[0] : '';
            $linkedin_url = !empty($socials[1]) ? $socials[1] : '';


            return [
                'nmls' => $nmls,
                'first_name' => $first_name,
                'last_name' => $last_name,
                'phone' => str_replace(["-", " ", "_", ".", ",", "(", ")"], "", $phone),
                'address' => $address,
                'zip' => $zip,
                'state' => $state,
                'facebook_url' => $facebook_url,
                'linkedin_url' => $linkedin_url,
                'website_url' => $website_url,
                'profile_url' => $url
            ];
        } catch (\GuzzleHttp\Exception\ConnectException $e) {
            $error = $e->getMessage();
        } catch (\GuzzleHttp\Exception\BadResponseException $e) {
            $error = $e->getMessage();
        } catch (RequestException $e) {
            $error = $e->getMessage();
        } catch (ClientException $e) {
            $error = $e->getMessage();
        } catch (\Exception $e) {
            $error = $e->getMessage();
        }
        
        if ($error) {
            echo $error;
        }
        return '';
    }

}
