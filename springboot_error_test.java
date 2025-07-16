// Main Application Class
@SpringBootApplication
public class BookStoreApplication {
    public static void main(String[] args) {
        SpringApplication.run(BookStoreApplication.class, args);
    }
}

// Entity Class - Book.java
@Entity
@Table(name = "books")
public class Book {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String title;
    
    @Column(nullable = false)
    private String author;
    
    @Column(nullable = false)
    private Double price;
    
    @Column(nullable = false)
    private Integer stock;
    
    // Missing constructors, getters, setters
}

// Repository Interface - BookRepository.java
@Repository
public interface BookRepository extends JpaRepository<Book, Long> {
    
    // Error: Incorrect query syntax
    @Query("SELECT b FROM Book b WHERE b.author = ?1 AND b.price < ?2")
    List<Book> findByAuthorAndPriceLessThan(String author, Double price);
    
    // Error: Missing @Param annotation
    @Query("SELECT b FROM Book b WHERE b.title LIKE %:title%")
    List<Book> findByTitleContaining(String title);
}

// Service Class - BookService.java
@Service
public class BookService {
    
    // Error: Missing @Autowired or constructor injection
    private BookRepository bookRepository;
    
    public List<Book> getAllBooks() {
        return bookRepository.findAll();
    }
    
    public Book getBookById(Long id) {
        // Error: Not handling Optional properly
        return bookRepository.findById(id);
    }
    
    public Book saveBook(Book book) {
        // Error: No validation
        return bookRepository.save(book);
    }
    
    public void deleteBook(Long id) {
        // Error: No existence check
        bookRepository.deleteById(id);
    }
    
    // Error: Transaction annotation missing for complex operation
    public Book updateBookStock(Long id, Integer newStock) {
        Book book = getBookById(id);
        book.setStock(newStock);
        return bookRepository.save(book);
    }
}

// Controller Class - BookController.java
@RestController
@RequestMapping("/api/books")
public class BookController {
    
    // Error: Missing @Autowired
    private BookService bookService;
    
    @GetMapping
    public List<Book> getAllBooks() {
        return bookService.getAllBooks();
    }
    
    @GetMapping("/{id}")
    public Book getBookById(@PathVariable Long id) {
        // Error: No exception handling
        return bookService.getBookById(id);
    }
    
    @PostMapping
    public Book createBook(@RequestBody Book book) {
        // Error: No validation
        return bookService.saveBook(book);
    }
    
    @PutMapping("/{id}")
    public Book updateBook(@PathVariable Long id, @RequestBody Book book) {
        // Error: Not setting the ID
        return bookService.saveBook(book);
    }
    
    @DeleteMapping("/{id}")
    public void deleteBook(@PathVariable Long id) {
        // Error: No response entity
        bookService.deleteBook(id);
    }
    
    // Error: Missing @GetMapping annotation
    public List<Book> searchBooks(@RequestParam String author, @RequestParam Double maxPrice) {
        return bookService.searchByAuthorAndPrice(author, maxPrice);
    }
}

// Configuration Class - DatabaseConfig.java
@Configuration
public class DatabaseConfig {
    
    // Error: Missing @Value annotation
    private String databaseUrl;
    
    // Error: Missing @Bean annotation
    public DataSource dataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(databaseUrl);
        config.setUsername("admin");
        config.setPassword("password");
        return new HikariDataSource(config);
    }
}

// Exception Handler Class - GlobalExceptionHandler.java
@ControllerAdvice
public class GlobalExceptionHandler {
    
    // Error: Wrong exception type
    @ExceptionHandler(Exception.class)
    public ResponseEntity<String> handleBookNotFound(BookNotFoundException ex) {
        return ResponseEntity.notFound().build();
    }
    
    // Error: Missing @ExceptionHandler annotation
    public ResponseEntity<String> handleValidationErrors(MethodArgumentNotValidException ex) {
        return ResponseEntity.badRequest().body("Validation failed");
    }
}

// Custom Exception - BookNotFoundException.java
public class BookNotFoundException extends RuntimeException {
    public BookNotFoundException(String message) {
        super(message);
    }
}

// Test Class - BookServiceTest.java
@SpringBootTest
public class BookServiceTest {
    
    // Error: Missing @MockBean
    private BookRepository bookRepository;
    
    @Autowired
    private BookService bookService;
    
    @Test
    public void testGetAllBooks() {
        // Error: No mock setup
        List<Book> books = bookService.getAllBooks();
        assertEquals(0, books.size());
    }
    
    @Test
    public void testGetBookById() {
        // Error: No mock setup for Optional
        Book book = bookService.getBookById(1L);
        assertNotNull(book);
    }
}

// Application Properties - application.yml
# Error: Incorrect YAML syntax and missing properties
spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password: 
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true
  # Error: Missing server port configuration
  # Error: Missing logging configuration

# pom.xml dependencies (partial)
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    
    <!-- Error: Missing version -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    
    <!-- Error: Wrong scope for H2 database -->
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <scope>test</scope>
    </dependency>
    
    <!-- Error: Missing test dependencies -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>