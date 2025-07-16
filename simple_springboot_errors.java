// Main Application Class - Application.java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

// Product Entity - Product.java
@Entity
@Table(name = "products")
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String name;
    
    @Column(nullable = false)
    private Double price;
    
    @Column(nullable = false)
    private Integer quantity;
    
    // Error: Missing default constructor
    public Product(String name, Double price, Integer quantity) {
        this.name = name;
        this.price = price;
        this.quantity = quantity;
    }
    
    // Error: Missing getters and setters
    public Long getId() { return id; }
    public String getName() { return name; }
    public Double getPrice() { return price; }
    public Integer getQuantity() { return quantity; }
    
    // Error: Missing setters
}

// Repository Interface - ProductRepository.java
@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    
    // Error: Method name doesn't follow naming convention
    List<Product> findByNameContains(String name);
    
    // Error: Should return Optional
    Product findByName(String name);
    
    // Error: Query has typo
    @Query("SELECT p FROM Product p WHERE p.price > :price")
    List<Product> findExpensiveProducts(@Param("pric") Double price);
}

// Service Class - ProductService.java
@Service
public class ProductService {
    
    // Error: Missing @Autowired or constructor injection
    private ProductRepository productRepository;
    
    public List<Product> getAllProducts() {
        return productRepository.findAll();
    }
    
    public Product getProductById(Long id) {
        // Error: Not handling Optional properly
        return productRepository.findById(id).get();
    }
    
    public Product saveProduct(Product product) {
        // Error: No validation
        return productRepository.save(product);
    }
    
    public void deleteProduct(Long id) {
        // Error: No existence check
        productRepository.deleteById(id);
    }
    
    public List<Product> searchProducts(String name) {
        // Error: Method name mismatch with repository
        return productRepository.findByNameContains(name);
    }
    
    public Product findByName(String name) {
        // Error: Not handling null return
        return productRepository.findByName(name);
    }
}

// Controller Class - ProductController.java
@RestController
@RequestMapping("/api/products")
public class ProductController {
    
    @Autowired
    private ProductService productService;
    
    @GetMapping
    public List<Product> getAllProducts() {
        return productService.getAllProducts();
    }
    
    @GetMapping("/{id}")
    public Product getProductById(@PathVariable Long id) {
        // Error: No exception handling
        return productService.getProductById(id);
    }
    
    @PostMapping
    public Product createProduct(@RequestBody Product product) {
        return productService.saveProduct(product);
    }
    
    @PutMapping("/{id}")
    public Product updateProduct(@PathVariable Long id, @RequestBody Product product) {
        // Error: Not setting the ID
        return productService.saveProduct(product);
    }
    
    @DeleteMapping("/{id}")
    public void deleteProduct(@PathVariable Long id) {
        productService.deleteProduct(id);
    }
    
    @GetMapping("/search")
    public List<Product> searchProducts(@RequestParam String name) {
        return productService.searchProducts(name);
    }
    
    // Error: Missing @GetMapping annotation
    public Product getProductByName(@RequestParam String name) {
        return productService.findByName(name);
    }
}

// Configuration Class - AppConfig.java
@Configuration
public class AppConfig {
    
    // Error: Missing @Bean annotation
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}

// Exception Class - ProductNotFoundException.java
public class ProductNotFoundException extends RuntimeException {
    public ProductNotFoundException(String message) {
        super(message);
    }
}

// Exception Handler - GlobalExceptionHandler.java
@ControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(ProductNotFoundException.class)
    public ResponseEntity<String> handleProductNotFound(ProductNotFoundException ex) {
        return ResponseEntity.notFound().build();
    }
    
    // Error: Wrong exception type
    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<String> handleGeneral(Exception ex) {
        return ResponseEntity.internalServerError().body("Something went wrong");
    }
}

// Test Class - ProductServiceTest.java
@SpringBootTest
public class ProductServiceTest {
    
    @Autowired
    private ProductService productService;
    
    // Error: Should be @MockBean
    @Mock
    private ProductRepository productRepository;
    
    @Test
    public void testGetAllProducts() {
        // Error: No mock setup
        List<Product> products = productService.getAllProducts();
        assertNotNull(products);
    }
    
    @Test
    public void testGetProductById() {
        // Error: No mock setup
        Product product = productService.getProductById(1L);
        assertNotNull(product);
    }
    
    @Test
    public void testSaveProduct() {
        Product product = new Product("Test Product", 99.99, 10);
        
        // Error: No mock setup
        Product saved = productService.saveProduct(product);
        assertNotNull(saved);
    }
}

// Application Properties - application.properties
# Error: Typo in property name
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=

# Error: Wrong property name
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.show-sql=true

# Error: Missing server port
# server.port=8080

# Error: Missing H2 console configuration
# spring.h2.console.enabled=true

# Maven Dependencies - pom.xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.example</groupId>
    <artifactId>product-service</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.1.0</version>
        <relativePath/>
    </parent>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        
        <!-- Error: Missing H2 database dependency -->
        
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>

// Data Initialization - DataLoader.java
@Component
public class DataLoader implements CommandLineRunner {
    
    // Error: Missing @Autowired
    private ProductRepository productRepository;
    
    @Override
    public void run(String... args) throws Exception {
        // Error: Will fail due to missing default constructor
        Product product1 = new Product("Laptop", 999.99, 5);
        Product product2 = new Product("Mouse", 29.99, 20);
        
        productRepository.save(product1);
        productRepository.save(product2);
    }
}