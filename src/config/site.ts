export interface PageConfig {
  title: string;
  slug: string;
  published: boolean;
  description: string;
}

export const pages: PageConfig[] = [
  {
    title: 'Home',
    slug: '/',
    published: true,
    description: 'The Greenway Band — Houston premium live wedding entertainment'
  },
  {
    title: 'Experience',
    slug: '/experience',
    published: true,
    description: 'What a Greenway night looks and feels like'
  },
  {
    title: 'Vocalists',
    slug: '/vocalists',
    published: false,
    description: 'Meet the voices of The Greenway Band'
  },
  {
    title: 'Reviews',
    slug: '/reviews',
    published: false,
    description: 'What our couples and planners say'
  },
  {
    title: 'FAQ',
    slug: '/faq',
    published: false,
    description: 'Common questions about booking The Greenway Band'
  },
  {
    title: 'Book',
    slug: '/book',
    published: true,
    description: 'Inquire about The Greenway Band for your event'
  }
];

export const siteConfig = {
  name: 'The Greenway Band',
  descriptor: 'The sound of a great night',
  url: 'https://greenway-website.netlify.app',
  email: 'adrian@greenwayband.com',
  phone: '(281) 467-1226',
  location: 'Houston, Texas',
  ogImage: '/og-image.jpg'
};
